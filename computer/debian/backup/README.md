# Off-box backup: borg + encrypted secrets (Debian 13)

LVM snapshots (lvm-snapshots note) + gark_home git snapshots (home-git-snapshot note) not backups — die with disk. This note off-box layer: borg for home + /etc, age for secrets.

## 1. Target

Pick one, set `BORG_REPO` below (adjust host/path):

```bash
# NAS over SSH (recommended; you have rsync/ssh to the NAS already):
export BORG_REPO='ssh://backup@nas.lan/srv/backup/gark'
# or a USB disk mounted at /mnt/backup:
# export BORG_REPO='/mnt/backup/gark.borg'
```

Init once: `pkexec apt install -y borgbackup age` (age from trixie), then `borg init --encryption=repokey-blake2 "$BORG_REPO"` (passphrase in keyring-backed password manager; repokey keeps key in repo, NAS alone not enough to decrypt).

## 2. What is backed up

- `/home/galmost` **minus** `Avalon-models` (134G — recover via sha256 manifest in ai/amd/avalon), `node_modules`, `__pycache__`, browser caches, `.cache`. Includes `~/.pi/agent/sessions` (agent session history).
- `/etc` (system config) — or etckeeper for tracked parts.
- Secrets, separately, age-encrypted before leaving machine:

```bash
age-keygen -o ~/.config/age/key.txt 2>/dev/null || age-keygen -o ~/.config/age/key.txt   # print pubkey once, store it
tar czf - ~/.pi/agent/auth.json ~/.ssh/id_ed25519_bitbucket ~/.local/share/keyrings ~/.gnupg ~/.config/gh \
  | age -r "$(grep '^# created' -B1 ~/.config/age/key.txt >/dev/null; awk '/public key/{print $NF}' ~/.config/age/key.txt 2>/dev/null || age-keygen -y ~/.config/age/key.txt)" \
  > "$HOME/.local/share/backups/secrets-$(date +%F).tar.gz.age"
# copy that file to the NAS; never back up ~/.config/age/key.txt itself to the NAS
```

Secrets never in git, never in borg unencrypted.

## 3. Run + schedule

```bash
borg create --stats --progress "$BORG_REPO"::"{hostname}-{now:%Y-%m-%d_%H:%M}" \
  /home/galmost /etc \
  --exclude '/home/galmost/Avalon-models' --exclude '*/node_modules' --exclude '*/__pycache__' \
  --exclude '/home/galmost/.cache' --exclude '/home/galmost/.local/share/Trash'
borg prune -v --list "$BORG_REPO" --keep-daily=7 --keep-weekly=4 --keep-monthly=6
borg compact "$BORG_REPO"
```

Automate with systemd user timer like gark-home-snapshot (see home-git-snapshot note): `~/.config/systemd/user/gark-borg.{service,timer}`, `OnCalendar=daily`, `Persistent=true`.

## 4. Restore drill (quarterly — a backup never restored is a rumor)

```bash
borg list "$BORG_REPO"                          # pick an archive
borg extract --dry-run "$BORG_REPO::gark-2026-11-25_00:00" home/galmost/.zshrc
mkdir /tmp/restore && cd /tmp/restore && borg extract "$BORG_REPO::gark-2026-11-25_00:00" home/galmost/.zshrc
# secrets: age -d -i ~/.config/age/key.txt secrets-2026-11-25.tar.gz.age | tar tzf -
```

## 5. Full disaster recovery order

1. Reinstall Debian 13 per setup index (computer/debian/README.md).
2. Restore home from gark_home git (clone gark_home, checkout) — dotfiles.
3. Restore packages: `dpkg --set-selections < galmost@GArk/packages/dpkg-selections.txt`.
4. borg extract home + /etc from NAS.
5. age-decrypt secrets back into place.
6. Re-download models per ai/amd/avalon/models-manifest.sha256.
7. LVM snapshot NOT in path — only pre-risk undo button.

## Source

- https://borgbackup.readthedocs.io/ , https://age-encryption.org/