# Off-box backup: borg + encrypted secrets (Debian 13)

LVM snapshots and gark_home git snapshots die with the disk. This is the off-box layer: borg for home + `/etc`, age for secrets.

## 1. Target

Pick one and set `BORG_REPO`:

```bash
export BORG_REPO='ssh://backup@nas.lan/srv/backup/gark'   # NAS over SSH (recommended)
# export BORG_REPO='/mnt/backup/gark.borg'                # or USB disk
```

```bash
pkexec apt install -y borgbackup age
borg init --encryption=repokey-blake2 "$BORG_REPO"
```

Passphrase in the keyring-backed password manager. `repokey` keeps the key inside the repo, so the NAS alone can decrypt — keep the passphrase out of the NAS.

## 2. What is backed up

- `/home/galmost` minus `Avalon-models` (134G; restore via sha256 manifest in `ai/amd/avalon`), `node_modules`, `__pycache__`, browser caches, `.cache`. Includes `~/.pi/agent/sessions`.
- `/etc` — or etckeeper for tracked parts.
- Secrets separately, age-encrypted before leaving the machine:

```bash
age-keygen -o ~/.config/age/key.txt          # pubkey line "# public key: age1..."
tar czf - ~/.pi/agent/auth.json ~/.ssh/id_ed25519_bitbucket ~/.local/share/keyrings ~/.gnupg ~/.config/gh \
  | age -r "$(age-keygen -y ~/.config/age/key.txt)" \
  > "$HOME/.local/share/backups/secrets-$(date +%F).tar.gz.age"
```

Copy that file to the NAS. Never back up `~/.config/age/key.txt` to the NAS. Secrets never in git, never in borg unencrypted.

## 3. Run + schedule

```bash
borg create --stats --progress "$BORG_REPO"::"{hostname}-{now:%Y-%m-%d_%H:%M}" \
  /home/galmost /etc \
  --exclude '/home/galmost/Avalon-models' --exclude '*/node_modules' --exclude '*/__pycache__' \
  --exclude '/home/galmost/.cache' --exclude '/home/galmost/.local/share/Trash'
borg prune -v --list "$BORG_REPO" --keep-daily=7 --keep-weekly=4 --keep-monthly=6
borg compact "$BORG_REPO"
```

Automate with `~/.config/systemd/user/gark-borg.{service,timer}` (`OnCalendar=daily`, `Persistent=true`), same shape as [home-git-snapshot](../home-git-snapshot/README.md).

## 4. Quarterly restore drill

A backup never restored is a rumor.

```bash
borg list "$BORG_REPO"
borg extract --dry-run "$BORG_REPO::gark-2026-11-25_00:00" home/galmost/.zshrc
mkdir /tmp/restore && cd /tmp/restore && borg extract "$BORG_REPO::gark-2026-11-25_00:00" home/galmost/.zshrc
age -d -i ~/.config/age/key.txt secrets-2026-11-25.tar.gz.age | tar tzf -
```

## 5. Full disaster recovery order

1. Reinstall Debian 13 per [setup index](../README.md).
2. Restore home from git: clone `gark_home`, `git checkout origin/main -- .`.
3. Restore packages: `dpkg --set-selections < galmost@GArk/packages/dpkg-selections.txt`.
4. `borg extract` home + `/etc` from the NAS.
5. age-decrypt secrets back into place.
6. Re-download models per `ai/amd/avalon/models-manifest.sha256`.
7. LVM snapshot is not in this path — pre-risk undo button only.

## Source

- https://borgbackup.readthedocs.io/
- https://age-encryption.org/
