# Digi Storage desktop client (CachyOS)

Digi Storage (RCS-RDS cloud) Electron/CEF client. Download requires Digi
credentials at https://storage.rcs-rds.ro/app/admin/places/connect-computer —
never put credentials in this repo or in git. Tarball:
`digistorage-decf8db-linux-x86_64.tar.gz` (~105 MB).

## 1. Install from local tarball

Bundled `installer.sh` is interactive (`read -p`) — replicate non-interactively:

```bash
mkdir -p ~/.digistorage-dist
tar xzf ~/Downloads/digistorage-decf8db-linux-x86_64.tar.gz -C ~/.digistorage-dist --strip-components=1
ldd ~/.digistorage-dist/storagegui | grep "not found"   # must be empty
```

## 2. Desktop entry + autostart (what installer.sh would write)

```bash
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/digistorage.desktop << 'EOF'
[Desktop Entry]
  Name=Digi Storage
  GenericName=Hybrid storage cloud
  Exec=/home/galmost/.digistorage-dist/storagegui
  Terminal=false
  Type=Application
  Icon=/home/galmost/.digistorage-dist/icon.png
  Categories=Network;FileTransfer;Internet;
EOF
cp ~/.local/share/applications/digistorage.desktop ~/.config/autostart/digistorage.desktop
update-desktop-database ~/.local/share/applications
```

## 3. Run / login

```bash
~/.digistorage-dist/storagegui        # or launch from app menu; autostarts on login
# first run: log in with Digi credentials in the GUI
```

## Troubleshooting

- `ldd ... | grep "not found"` non-empty — install missing libs (udev/gtk) via `pkexec pacman -S ...`.
- App won't start under Wayland — run with `--ozone-platform=x11` fallback: edit Exec line.
- `~/.digistorage-dist` (~110 MB binary) is NOT tracked by home git (default-deny `.gitignore`) — re-extract from tarball on restore.

## Source

- https://storage.rcs-rds.ro/app/admin/places/connect-computer (login required)
