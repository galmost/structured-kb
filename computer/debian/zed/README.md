# Zed Editor Install (Debian / Ubuntu)

## 1. Install

```bash
curl -fsSL https://zed.dev/install.sh | sh
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
pkexec apt install -y mesa-vulkan-drivers libvulkan1
```

## 3. Uninstall

```bash
zed --uninstall
```

## Source

- [Zed installation — Linux](https://zed.dev/docs/installation#linux)
- [Zed on Linux](https://zed.dev/docs/linux)
