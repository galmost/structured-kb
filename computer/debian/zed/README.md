# Zed Editor Setup (Debian / Ubuntu)

Installs the Zed code editor via the official install script and applies the
shared configuration from `ide/zed/` in this repo. Per
[Zed Linux docs](https://zed.dev/docs/installation#linux).

## 1. Install

```bash
curl -fsSL https://zed.dev/install.sh | sh
```

The script downloads a prebuilt `.tar.gz` (~86 MB), extracts it to
`~/.local/zed.app/`, and symlinks `zed` into `~/.local/bin/`. Supports
x86_64 and AArch64 on Debian, Ubuntu, Arch, Fedora, and more.

Verify:

```bash
zed --version
```

Preview channel (updates ~1 week ahead of stable):

```bash
curl -fsSL https://zed.dev/install.sh | ZED_CHANNEL=preview sh
```

Pin a version:

```bash
curl -fsSL https://zed.dev/install.sh | ZED_VERSION=0.216.0 sh
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
Install Vulkan drivers if missing:

```bash
sudo apt install -y mesa-vulkan-drivers
```

## Uninstall

```bash
zed --uninstall
```

## Source

- [Zed installation — Linux](https://zed.dev/docs/installation#linux)
- [Zed on Linux](https://zed.dev/docs/linux)
