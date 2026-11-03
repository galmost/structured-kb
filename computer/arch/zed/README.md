# Zed Editor Install (Arch Linux)

## 1. Install

Official script (recommended):

```bash
curl -fsSL https://zed.dev/install.sh | sh
```

Or AUR:

```bash
yay -S zed-editor-bin
# or
paru -S zed-editor-bin
```

Verify:

```bash
zed --version
```

Preview channel:

```bash
curl -fsSL https://zed.dev/install.sh | ZED_CHANNEL=preview sh
```

Pin a version:

```bash
curl -fsSL https://zed.dev/install.sh | ZED_VERSION=0.216.0 sh
```

## 2. Requirements

Zed needs Vulkan-capable driver. Check `~/.local/share/zed/logs/Zed.log`
for `Using GPU:`.

```bash
sudo pacman -S vulkan-radeon   # AMD
sudo pacman -S vulkan-intel   # Intel
sudo pacman -S nvidia-utils    # NVIDIA
```

## 3. Uninstall

```bash
zed --uninstall
```

## Source

- [Zed installation — Linux](https://zed.dev/docs/installation#linux)
- [Zed on Linux](https://zed.dev/docs/linux)
