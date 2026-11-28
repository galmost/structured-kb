# rclone — Systemd Mount (Arch Linux)

[rclone](https://rclone.org/) mounts cloud storage (Google Drive, S3, Dropbox, OneDrive, ...) as a filesystem via `rclone mount`.

## 1. Install and configure

```bash
pacman -S rclone fuse3
rclone config          # add a remote; stored in ~/.config/rclone/rclone.conf
```

## 2. Systemd user mount unit

`~/.config/systemd/user/rclone-<remote>.service`:

```ini
[Unit]
Description=rclone mount for <remote>
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/bin/rclone mount <remote>: /path/to/mountpoint \
  --vfs-cache-mode writes \
  --vfs-cache-max-size 500M \
  --log-level INFO
ExecStop=/bin/fusermount -u /path/to/mountpoint
Restart=on-failure

[Install]
WantedBy=default.target
```

```bash
mkdir -p /path/to/mountpoint
systemctl --user enable --now rclone-<remote>.service
```

## Notes

- `--vfs-cache-mode writes` balances speed and compatibility; raise `--vfs-cache-max-size` for heavy write workloads.
- Throttle bandwidth with `--bwlimit`.

## Source

- [Systemd rclone mount guide](https://github.com/rclone/rclone/wiki/Systemd-rclone-mount)
- [rclone docs](https://rclone.org/docs/)
