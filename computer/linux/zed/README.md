# Zed Editor Setup (Linux)

Zed is a code editor with GPU-accelerated UI. The official install script
works on most Linux distributions. Shared configuration lives in `ide/zed/`
in this repo.

## Install

Distro-specific install steps:

- Debian / Ubuntu: see [computer/debian/zed/README.md](../../debian/zed/README.md)
- Arch: see [computer/arch/zed/README.md](../../arch/zed/README.md)

## Apply shared configuration

Copy the repo's Zed config into `~/.config/zed/`:

```bash
mkdir -p ~/.config/zed
cp ide/zed/settings.json ~/.config/zed/settings.json
cp ide/zed/keymap.json ~/.config/zed/keymap.json
```

Restart Zed to apply. Config source of truth lives in `ide/zed/` — edit
there, then re-copy.

## Uninstall

```bash
zed --uninstall
```

## Source

- [Zed installation — Linux](https://zed.dev/docs/installation#linux)
- [Zed on Linux](https://zed.dev/docs/linux)
