# Zed Editor Setup (Linux)

Installs the Zed code editor via the official install script and applies the
shared configuration from `ide/zed/` in this repo. Works on Debian, Ubuntu,
Arch, Fedora, and most Linux distributions. Per
[Zed Linux docs](https://zed.dev/docs/installation#linux).

## 1. Install

Official install script: downloads prebuilt `.tar.gz`, extracts to
`~/.local/zed.app/`, symlinks `zed` into `~/.local/bin/`. Supports x86_64
and AArch64.

```bash
curl -fsSL https://zed.dev/install.sh | sh
```

Verify:

```bash
zed --version
```

### Debian / Ubuntu

If using pkexec:

```bash
curl -fsSL https://zed.dev/install.sh | ZED_INSTALL_DIR=/opt/zed sh
pkexec ln -s /opt/zed/zed /usr/local/bin/zed
```

Preview channel (updates ~1 week ahead of stable):

```bash
curl -fsSL https://zed.dev/install.sh | ZED_CHANNEL=preview sh
```

Pin a version:

```bash
curl -fsSL https://zed.dev/install.sh | ZED_VERSION=0.216.0 sh
```

### Arch Linux

Use the official install script or AUR package:

```bash
# Official script (recommended)
curl -fsSL https://zed.dev/install.sh | sh

# Or AUR (may lag behind releases)
yay -S zed-editor-bin
# or
paru -S zed-editor-bin
```

## 2. Apply shared configuration

Copy the repo's Zed config into `~/.config/zed/`:

```bash
mkdir -p ~/.config/zed
cp ide/zed/settings.json ~/.config/zed/settings.json
cp ide/zed/keymap.json ~/.config/zed/keymap.json
```

Restart Zed to apply. Config source of truth lives in `ide/zed/` — edit
there, then re-copy.

## 3. Requirements

Zed renders with the GPU and needs a Vulkan-capable driver. Check
`~/.local/share/zed/logs/Zed.log` for `Using GPU:` if it fails to start.

### Debian / Ubuntu

```bash
pkexec apt install -y mesa-vulkan-drivers libvulkan1
```

### Arch Linux

```bash
sudo pacman -S vulkan-radeon  # AMD
sudo pacman -S vulkan-intel  # Intel
sudo pacman -S nvidia-utils   # NVIDIA
```

## Uninstall

```bash
zed --uninstall
```

Removes `~/.local/zed.app/` and the symlink in `~/.local/bin/`.

## Source

- [Zed installation — Linux](https://zed.dev/docs/installation#linux)
- [Zed on Linux](https://zed.dev/docs/linux)
