# Local Backup and Rollback (CachyOS rolling)

Local-first recovery strategy for CachyOS desktop. Layers: btrfs snapshots (instant rollback) + home git snapshot (config timeline) + off-box (WIP). Goal: recover from agent breaks or full system wipe.

## 1. Overview - Layered Local Recovery

| Layer | Tool | Scope | Retention | Trigger | Restore Speed |
|---|---|---|---|---|---|
| 1 | Btrfs snapshots (snapper) | Full system (`/`) | 3 monthly | `snapper-timeline.timer` | Instant |
| 2 | Btrfs agent snapshots | Home (`/home`) | 3 newest | Startup + on-demand | Instant |
| 3 | Home git snapshot | Dotfiles, configs, package lists | Unlimited (Bitbucket) | Daily systemd timer | Git checkout |
| 4 | Off-box backup | Home + /etc + secrets | WIP | WIP | WIP |
| 5 | Secrets backup | Encrypted tarball | WIP | WIP | WIP |

**Rollback priority:** Agent snapshots (immediate home restore) → Snapper (system) → Home git (config) → Full reinstall.

## 2. Snapper Monthly Snapshots (Full System)

Automatic monthly snapshots of root (`/`) via snapper. Keeps last 3.

### 2.1 Configuration

File: `/etc/snapper/configs/root`

```ini
TIMELINE_CREATE="yes"
TIMELINE_LIMIT_MONTHLY="3"
TIMELINE_LIMIT_HOURLY="0"
TIMELINE_LIMIT_DAILY="0"
TIMELINE_LIMIT_WEEKLY="0"
TIMELINE_LIMIT_YEARLY="0"
```

### 2.2 Enable

```bash
pkexec systemctl enable --now snapper-timeline.timer
pkexec systemctl status snapper-timeline.timer
```

### 2.3 Location

Snapshots stored in `/.snapshots/` (root-only access).

### 2.4 List Snapshots

```bash
pkexec btrfs subvolume list /.snapshots
# or
pkexec snapper list
```

### 2.5 Restore

**Full system restore (disaster recovery):**
```bash
# Boot live USB, mount btrfs
mount /dev/nvme0n1p2 /mnt
# Delete current root subvolume
btrfs subvolume delete /mnt/@
# Snapshot the snapshot to new root
btrfs subvolume snapshot /mnt/.snapshots/N/snapshot /mnt/@
# Reboot
```

**Single file restore:**
```bash
# Mount snapshot
pkexec mount -o subvol=/.snapshots/N/snapshot /dev/nvme0n1p2 /mnt/restore
# Copy file
cp /mnt/restore/path/to/file /path/to/file
# Unmount
pkexec umount /mnt/restore
```

## 3. Agent Startup Snapshots (Home Directory)

Dedicated snapshots of `/home` for agent rollback. Keeps last 3. Triggers: system startup + on-demand.

### 3.1 Script

File: `/usr/local/bin/btrfs-agent-snapshot`

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

Make executable:
```bash
pkexec chmod +x /usr/local/bin/btrfs-agent-snapshot
```

### 3.2 Systemd Service (Startup Trigger)

File: `/etc/systemd/system/btrfs-agent-snapshot.service`

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

Enable:
```bash
pkexec systemctl enable btrfs-agent-snapshot.service
```

### 3.3 On-Demand Trigger (For Agents)

Agents can trigger snapshot before risky operations:
```bash
pkexec /usr/local/bin/btrfs-agent-snapshot
```

### 3.4 Location

Snapshots stored in `/.snapshots/agent/` (root-only access).

### 3.5 List Snapshots

```bash
pkexec btrfs subvolume list /.snapshots/agent
```

### 3.6 Restore

**Single file restore:**
```bash
# Find snapshot with file
pkexec find /.snapshots/agent -name "filename" -type f
# Copy from snapshot
pkexec cp /.snapshots/agent/home-*/path/to/file /home/galmost/path/to/file
```

**Full home restore:**
```bash
# Mount snapshot
pkexec mount -o subvol=/.snapshots/agent/home-*/ /dev/nvme0n1p2 /mnt/restore
# Rsync to home
rsync -a /mnt/restore/galmost/ /home/galmost/
pkexec umount /mnt/restore
```

## 4. Home Git Snapshot

Daily git commits of allowlisted dotfiles to Bitbucket. Covers configs, package lists, scripts.

### 4.1 Existing Setup

Already configured. See `computer/cachyos/home-git-snapshot/README.md` for details.

**What's tracked:**
- Dotfiles: `~/.zshrc`, `~/.gitconfig`, `~/.pi/agent/settings.json`, `~/.pi/agent/models-store.json`
- Configs: `~/.config/...` (allowlisted)
- Package lists: `galmost@GCachyDeck/packages/pacman-explicit.txt`, `pacman-foreign.txt`
- Scripts: `galmost@GCachyDeck/bin/*`

**What's NOT tracked (secrets):**
- `~/.pi/agent/auth.json`
- `~/.ssh/id_*`
- `~/.config/gh/`
- `~/.gnupg`
- `~/.local/share/keyrings/`

### 4.2 Restore

```bash
cd ~
git fetch origin
git checkout origin/main -- .           # Restore all tracked files
git checkout origin/main -- <path>     # Restore single file
```

### 4.3 Reinstall from Git

```bash
# After fresh CachyOS install
cd ~
git clone git@ssh.bitbucket.org:galmost/gcachydeck_home.git .
git checkout origin/main -- .

# Install packages
pkexec pacman -S --needed $(cat galmost@GCachyDeck/packages/pacman-explicit.txt)
yay -S $(cat galmost@GCachyDeck/packages/pacman-foreign.txt) 2>/dev/null || true

# Enable services
systemctl --user enable --now gcachydeck-home-snapshot.timer
pkexec systemctl enable btrfs-agent-snapshot.service
```

## 5. Full Reinstall Procedure

**When:** System is completely wiped or unrecoverable.

### 5.1 Install CachyOS

1. Boot live USB
2. Partition disk with btrfs
3. Create subvolumes:
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
4. Install CachyOS to `/mnt`
5. Reboot

### 5.2 Restore Home

```bash
cd ~
git clone git@ssh.bitbucket.org:galmost/gcachydeck_home.git .
git checkout origin/main -- .
```

### 5.3 Install Packages

```bash
pkexec pacman -S --needed $(cat galmost@GCachyDeck/packages/pacman-explicit.txt)
yay -S $(cat galmost@GCachyDeck/packages/pacman-foreign.txt) 2>/dev/null || true
```

### 5.4 Restore Services

```bash
systemctl --user enable --now gcachydeck-home-snapshot.timer
pkexec systemctl enable btrfs-agent-snapshot.service
pkexec systemctl enable snapper-timeline.timer
```

### 5.5 Verify

```bash
# Check snapper
pkexec snapper list

# Check agent snapshots
pkexec btrfs subvolume list /.snapshots/agent

# Check git snapshot
systemctl --user status gcachydeck-home-snapshot.timer
```

## 6. Reinstall Test Procedure (Quarterly)

**Drill:** Verify full recovery works without real disaster.

### 6.1 Test Full Reinstall

1. **Backup current state:**
   ```bash
   pkexec btrfs subvolume snapshot / /.snapshots/manual-pre-test-$(date +%F)
   ```

2. **Wipe and reinstall:**
   - Boot live USB
   - Repartition, reinstall CachyOS
   - Follow Full Reinstall Procedure (section 5)

3. **Verify:**
   - [ ] Zsh loads with correct theme
   - [ ] Pi agent starts
   - [ ] Configs intact (`~/.zshrc`, `~/.pi/agent/settings.json`)
   - [ ] Package lists match
   - [ ] Services enabled

4. **Document:**
   ```bash
   echo "Reinstall test: $(date) - PASSED/FAILED" >> ~/reinstall-test-log.txt
   git add ~/reinstall-test-log.txt
   git commit -m "chore: reinstall test log"
   git push
   ```

5. **Rollback:**
   ```bash
   # If test machine, keep reinstall
   # If production, restore from pre-test snapshot
   ```

## 7. Agent-Specific Rollback

**When:** Agent run breaks something in home directory.

### 7.1 Before Risky Agent Run

```bash
# Manual snapshot
pkexec /usr/local/bin/btrfs-agent-snapshot

# Or let startup service handle it (runs at boot)
```

### 7.2 If Something Breaks

```bash
# List agent snapshots
pkexec btrfs subvolume list /.snapshots/agent

# Identify broken file
ls -la ~/.pi/agent/

# Restore single file from latest snapshot
pkexec cp /.snapshots/agent/home-*/path/to/file ~/.path/to/file

# Or restore entire home from snapshot
pkexec mount -o subvol=/.snapshots/agent/home-*/ /dev/nvme0n1p2 /mnt/restore
rsync -a /mnt/restore/galmost/ /home/galmost/
pkexec umount /mnt/restore
```

### 7.3 Full Agent Config Restore

```bash
# From git (if dotfiles tracked)
cd ~
git checkout origin/main -- .pi/agent/

# Or from btrfs snapshot
pkexec cp -r /.snapshots/agent/home-*/galmost/.pi/agent/* ~/.pi/agent/
```

## 8. Off-box Backup (WIP)

**Status:** Not implemented. Placeholder for future work.

**Options:**
- **Tool:** borg (like Debian setup) or restic
- **Target:** NAS over SSH or USB disk
- **Encryption:** repokey or keyfile
- **Scope:** `/home/galmost` (minus exclusions), `/etc`
- **Exclusions:** Cache, node_modules, __pycache__, browser caches, models
- **Schedule:** Weekly systemd timer

**Secrets:** age-encrypted tarball, stored separately.

## 9. Secrets Backup (WIP)

**Status:** Not implemented. Critical for full recovery.

**Files to backup:**
- `~/.pi/agent/auth.json`
- `~/.ssh/id_*` (Bitbucket, GitHub, etc.)
- `~/.config/gh/hosts.yml`
- `~/.gnupg`
- `~/.local/share/keyrings/`

**Method:**
```bash
age-keygen -o ~/.config/age/key.txt
tar czf - ~/.pi/agent/auth.json ~/.ssh/id_* ~/.config/gh ~/.gnupg ~/.local/share/keyrings \
  | age -r "$(age-keygen -y ~/.config/age/key.txt)" \
  > "$HOME/.local/share/backups/secrets-$(date +%F).tar.gz.age"
```

**Storage:** Copy to NAS or off-box target. Never in git.

## 10. Quick Reference

| Action | Command |
|---|---|
| List snapper snapshots | `pkexec snapper list` |
| List agent snapshots | `pkexec btrfs subvolume list /.snapshots/agent` |
| Create manual agent snapshot | `pkexec /usr/local/bin/btrfs-agent-snapshot` |
| Restore single file from agent snapshot | `pkexec cp /.snapshots/agent/home-*/path /home/galmost/path` |
| Restore from git | `cd ~ && git checkout origin/main -- <path>` |
| Full home restore from git | `cd ~ && git checkout origin/main -- .` |
| Full reinstall | See section 5 |

## Source

- btrfs: https://btrfs.readthedocs.io/
- snapper: https://github.com/openSUSE/snapper
- Adapted from Debian backup note: `computer/debian/backup/README.md`
