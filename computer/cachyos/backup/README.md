# Local Backup and Rollback (CachyOS rolling)

Local-first recovery for agent damage and full wipes. Layers: btrfs snapshots (instant rollback), home git snapshot (config timeline), off-box (WIP).

## 1. Layers

| Layer | Tool | Scope | Retention | Trigger | Restore speed |
|---|---|---|---|---|---|
| 1 | Btrfs snapshots (snapper) | `/` | 3 monthly | `snapper-timeline.timer` | Instant |
| 2 | Btrfs agent snapshots | `/home` | 3 newest | Startup + on-demand | Instant |
| 3 | Home git snapshot | Dotfiles, configs, package lists | Unlimited (Bitbucket) | Daily user timer | Git checkout |
| 4 | Off-box backup | Home + `/etc` + secrets | WIP (§8) | WIP | WIP |

**Restore priority:** agent snapshots (home) → snapper (system) → home git (configs) → full reinstall.

## 2. Snapper — monthly full-system snapshots

`/etc/snapper/configs/root`:

```ini
TIMELINE_CREATE="yes"
TIMELINE_LIMIT_MONTHLY="3"
TIMELINE_LIMIT_HOURLY="0"
TIMELINE_LIMIT_DAILY="0"
TIMELINE_LIMIT_WEEKLY="0"
TIMELINE_LIMIT_YEARLY="0"
```

```bash
pkexec systemctl enable --now snapper-timeline.timer
pkexec snapper list                    # snapshots live in /.snapshots/ (root-only)
pkexec btrfs subvolume list /.snapshots
```

### Restore

Single file:

```bash
pkexec mount -o subvol=/.snapshots/N/snapshot /dev/nvme0n1p2 /mnt/restore
cp /mnt/restore/path/to/file /path/to/file
pkexec umount /mnt/restore
```

Full system (boot live USB, snapshot N = chosen `/` snapshot):

```bash
mount /dev/nvme0n1p2 /mnt
btrfs subvolume delete /mnt/@
btrfs subvolume snapshot /mnt/.snapshots/N/snapshot /mnt/@
# reboot
```

## 3. Agent snapshots of /home

Script `/usr/local/bin/btrfs-agent-snapshot` (chmod +x via `pkexec chmod +x /usr/local/bin/btrfs-agent-snapshot`):

```bash
#!/bin/bash
set -euo pipefail

SNAP_DIR="/.snapshots/agent"
SNAP_NAME="home-$(date +%F-%H%M)"

mkdir -p "$SNAP_DIR"

btrfs subvolume snapshot /home "$SNAP_DIR/$SNAP_NAME"

# Get all home-* snapshots sorted by subvolume ID (oldest first)
mapfile -t all_snaps < <(btrfs subvolume list "$SNAP_DIR" | awk '$NF ~ /home-/ {print $NF}')

# Extract just the filename part (remove "agent/" prefix)
for i in "${!all_snaps[@]}"; do
    all_snaps[i]="${all_snaps[i]#agent/}"
done

# Delete all except last 3
for ((i=0; i<${#all_snaps[@]}-3; i++)); do
    btrfs subvolume delete "$SNAP_DIR/${all_snaps[i]}" || echo "WARN: delete failed $SNAP_DIR/${all_snaps[i]}" >&2
done
```

Startup trigger `/etc/systemd/system/btrfs-agent-snapshot.service`:

```ini
[Unit]
Description=Btrfs agent snapshot on startup
After=local-fs.target
Before=multi-user.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/btrfs-agent-snapshot

[Install]
WantedBy=multi-user.target
```

```bash
pkexec systemctl enable btrfs-agent-snapshot.service
pkexec /usr/local/bin/btrfs-agent-snapshot        # on-demand (agents: before risky ops)
pkexec btrfs subvolume list /.snapshots/agent     # list
```

### Restore

Single file — copy from latest snapshot that has it:

```bash
pkexec find /.snapshots/agent -name "filename" -type f
pkexec cp /.snapshots/agent/home-*/path/to/file /home/galmost/path/to/file
```

Full home:

```bash
pkexec mount -o subvol=/.snapshots/agent/home-*/ /dev/nvme0n1p2 /mnt/restore
rsync -a /mnt/restore/galmost/ /home/galmost/
pkexec umount /mnt/restore
```

## 4. Home git snapshot

Daily commits of allowlisted dotfiles to Bitbucket. Full setup: [home-git-snapshot/](../home-git-snapshot/README.md).

Tracked: `~/.zshrc`, `~/.gitconfig`, `~/.pi/agent/settings.json`, `~/.pi/agent/models-store.json`, allowlisted `~/.config/...`, `galmost@GCachyDeck/packages/pacman-{explicit,foreign}.txt`, `galmost@GCachyDeck/bin/*`.

Not tracked (secrets): `~/.pi/agent/auth.json`, `~/.ssh/id_*`, `~/.config/gh/`, `~/.gnupg`, `~/.local/share/keyrings/`.

```bash
cd ~
git fetch origin
git checkout origin/main -- .           # all tracked files
git checkout origin/main -- <path>      # one file
```

## 5. Full reinstall

1. Boot live USB, create btrfs subvolumes, install CachyOS to `/mnt`, reboot:

```bash
btrfs subvolume create /mnt/@
btrfs subvolume create /mnt/@home
btrfs subvolume create /mnt/@root
btrfs subvolume create /mnt/@srv
btrfs subvolume create /mnt/@cache
btrfs subvolume create /mnt/@tmp
btrfs subvolume create /mnt/@log
btrfs subvolume create /mnt/.snapshots
```

2. Restore home and packages:

```bash
cd ~
git clone git@ssh.bitbucket.org:galmost/gcachydeck_home.git .
git checkout origin/main -- .
pkexec pacman -S --needed $(cat galmost@GCachyDeck/packages/pacman-explicit.txt)
yay -S $(cat galmost@GCachyDeck/packages/pacman-foreign.txt) 2>/dev/null || true
```

3. Restore services and verify:

```bash
systemctl --user enable --now gcachydeck-home-snapshot.timer
pkexec systemctl enable btrfs-agent-snapshot.service
pkexec systemctl enable snapper-timeline.timer

pkexec snapper list
pkexec btrfs subvolume list /.snapshots/agent
systemctl --user status gcachydeck-home-snapshot.timer
```

## 6. Quarterly reinstall drill

Never-restored backup is a rumor. Snapshot first, then follow §5 on the machine, verify:

- Zsh loads with correct theme
- Pi agent starts
- `~/.zshrc`, `~/.pi/agent/settings.json` intact
- Package lists match
- Services enabled

```bash
pkexec btrfs subvolume snapshot / /.snapshots/manual-pre-test-$(date +%F)   # rollback point
echo "Reinstall test: $(date) - PASSED/FAILED" >> ~/reinstall-test-log.txt
git add ~/reinstall-test-log.txt && git commit -m "chore: reinstall test log" && git push
```

Rollback: production machine → restore from pre-test snapshot; throwaway machine → keep reinstall.

## 7. Agent rollback

```bash
pkexec /usr/local/bin/btrfs-agent-snapshot               # before risky run (startup service also covers boot)
pkexec btrfs subvolume list /.snapshots/agent            # pick snapshot
pkexec cp /.snapshots/agent/home-*/path/to/file ~/path/to/file   # one file
cd ~ && git checkout origin/main -- .pi/agent/           # or full config from git
```

Full home restore: §3.

## 8. Off-box backup and secrets (WIP)

Not implemented yet. Planned:

- **Tool:** borg (like the Debian setup) or restic. **Target:** NAS over SSH or USB disk. **Encryption:** repokey/keyfile.
- **Scope:** `/home/galmost` minus caches, `node_modules`, `__pycache__`, browser caches, models; plus `/etc`. **Schedule:** weekly systemd timer.
- **Secrets:** age-encrypted tarball of `~/.pi/agent/auth.json`, `~/.ssh/id_*`, `~/.config/gh/hosts.yml`, `~/.gnupg`, `~/.local/share/keyrings/`. Never in git, never off-box unencrypted.

```bash
age-keygen -o ~/.config/age/key.txt
tar czf - ~/.pi/agent/auth.json ~/.ssh/id_* ~/.config/gh ~/.gnupg ~/.local/share/keyrings \
  | age -r "$(age-keygen -y ~/.config/age/key.txt)" \
  > "$HOME/.local/share/backups/secrets-$(date +%F).tar.gz.age"
```

## 9. Quick reference

| Action | Command |
|---|---|
| List snapper snapshots | `pkexec snapper list` |
| List agent snapshots | `pkexec btrfs subvolume list /.snapshots/agent` |
| Create agent snapshot | `pkexec /usr/local/bin/btrfs-agent-snapshot` |
| Restore one file from agent snapshot | `pkexec cp /.snapshots/agent/home-*/path /home/galmost/path` |
| Restore one file from git | `cd ~ && git checkout origin/main -- <path>` |
| Restore everything tracked from git | `cd ~ && git checkout origin/main -- .` |

## Source

- btrfs: https://btrfs.readthedocs.io/
- snapper: https://github.com/openSUSE/snapper
- Adapted from Debian backup note: `computer/debian/backup/README.md`
