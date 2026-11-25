# Debian Setup Index (Debian 13 "trixie")

Agreed target state for a Debian desktop/dev box, distilled from the notes
in this folder plus the shared notes in `computer/linux/` and `ide/zed/`.
Each topic has its own folder with install commands, verification and
troubleshooting; this file is the map and the checklist.

There is no strict install order — every item is an independent package or
repo install. Prerequisites first, then anything else in any order.

## Prerequisites (base)

Run once on a fresh install, as root. `pkexec` is used throughout these
notes instead of `sudo` because `sudo` prompts for a password in a
non-interactive shell while `pkexec` authenticates via polkit:

```bash
pkexec apt install -y sudo curl gnupg git ca-certificates
pkexec usermod -aG sudo "$USER"   # log in again afterwards
pkexec apt install -y build-essential   # native npm modules (bcrypt, sharp, ...)
```

Verified on this host: curl 8.14.1, gnupg 2.4.7, git 2.47.3,
build-essential 12.12, pkexec 126, user in the `sudo` group.

## Agreed install set (desktop/dev)

| Component | Folder | Verified on trixie |
|---|---|---|
| Zsh + OMZ + Powerlevel10k | [zsh/](zsh/README.md), shared: [../linux/zsh/](../linux/zsh/README.md) | zsh 5.9-8+b24, login shell `/usr/bin/zsh`, p10k theme + plugins |
| Neovim (as `vi`/`vim`) | [nvim/](nvim/README.md) | NVIM v0.10.4, `vi`/`vim` alternatives point to `/usr/bin/nvim` |
| Zed editor + Vulkan + shared config | [zed/](zed/README.md), shared: [../linux/zed/](../linux/zed/README.md), config: [../../ide/zed/](../../ide/zed/README.md) | Zed 1.27.0, mesa-vulkan-drivers 25.0.7, libvulkan1 |
| Brave browser | [brave/](brave/README.md), shared: [../linux/brave/](../linux/brave/README.md) | Brave 156.1.98.63 via `brave-browser-release.list` |
| Node.js LTS (NodeSource) | [nodejs/](nodejs/README.md) | node v24.22.2, npm 11.19.1 via `nodesource.sources` |
| rsync (Zed remote dev) | [rsync/](rsync/README.md) | rsync 3.5.0, protocol 32 |
| aria2c (segmented downloads) | [aria2c/](aria2c/README.md) | aria2 1.37.0 |
| Wake-on-LAN | [wake-on-lan/](wake-on-lan/README.md) | ethtool 6.14.2, `Wake-on: g` and NetworkManager `802-3-ethernet.wake-on-lan: magic` on `enp11s0` |

Not in the desktop/dev set: the `ai/` notes. `ai/amd/avalon/` and
`ai/mistral/` describe the ROCm/llama.cpp stack and Vibe local-model
config for AMD RDNA3/4 render hosts, not this box.

## Applying shared configuration

- Shell: follow [../linux/zsh/](../linux/zsh/README.md) after installing
  zsh (see [zsh/](zsh/README.md) section 3).
- Zed: copy the repo config over the local one, it is the source of truth:

```bash
mkdir -p ~/.config/zed
cp ide/zed/settings.json ~/.config/zed/settings.json
cp ide/zed/keymap.json ~/.config/zed/keymap.json
```

## Source

- Debian 13 (trixie) package pages: https://packages.debian.org/trixie/
