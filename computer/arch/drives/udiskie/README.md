# udiskie Setup (Arch Linux)

Tray app for removable devices: shows mounts, mounts/unmounts on click. See §4 for secure automount-off config.

## 1. Install

```bash
sudo pacman -S udiskie
```

## 2. Configuration

Create or edit `~/.config/udiskie/config.yml`. Secure defaults: no automount, `nosuid`/`nodev`/`noexec`:

```yaml
program_options:
  tray: true              # show tray icon
  automount: false        # require manual mounting
  automount_open: false
  notify: true
  notify_all: false
  file_manager: thunar    # or nautilus, dolphin, pcmanfm, etc.
  mount_options:
    defaults:
      - noatime
      - nodiratime
      - nosuid
      - nodev
      - noexec
      - uid=1000
      - gid=1000
```

### Security-Focused Configuration

For enhanced security, disable automount and require manual mounting:

```yaml
program_options:
  # DISABLE automatic mounting for security
  automount: false
  automount_open: false
  tray: true
  notify: true
  notify_all: true
  mount_options:
    defaults:
      - noatime
      - nodiratime
      - nosuid
      - nodev
      - noexec
      - uid=1000
      - gid=1000
```

### Per-filesystem and per-device options

```yaml
mount_options:
  defaults:
    - umask=022
  ntfs:
    - windows_names
    - uid=1000
    - gid=1000
  vfat:
    - uid=1000
    - gid=1000
    - utf8
    - shortname=mixed

device_options:
  auto_mount:
    - /dev/sda1
    - /dev/sdb1
  ignore:
    - /dev/loop*
    - /dev/sr*
```

## 3. Autostart + usage

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/udiskie.desktop << EOF
[Desktop Entry]
Type=Application
Name=Udiskie
Exec=udiskie --tray
X-GNOME-Autostart-enabled=true
EOF
```

Manual start: `udiskie --tray &`. Tray: left-click lists devices, right-click mounts/unmounts/ejects, hover shows info.

## 4. Troubleshooting

### Tray icon not appearing

```bash
pgrep -a udiskie
pacman -Q udisks2 gvfs
groups     # user must be in storage group
```

Add `storage` to the user (`sudo usermod -aG storage $USER`) and apply with `newgrp storage`.

### Devices not appearing

```bash
systemctl --user status udisks2
udiskie --verbose
udisksctl mount -b /dev/sdX1
```

### Permission issues

```bash
sudo usermod -aG storage,optical,uucp $USER
newgrp storage
```

## Source

- [Udiskie GitHub](https://github.com/coldfix/udiskie)
- [Arch Wiki - Udisks](https://wiki.archlinux.org/title/Udisks)
- [Arch Wiki - Removable media](https://wiki.archlinux.org/title/Removable_media)
