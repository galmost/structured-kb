# CachyOS Setup Index (CachyOS rolling, Arch-based)

Target state for this CachyOS desktop/dev box. CachyOS-specific notes live
here; generic Arch notes stay in `computer/arch/`, shared Linux notes in
`computer/linux/`. Each topic folder has commands, check, fix. This file is
map and checklist.

No strict order. Every item independent.

## 1. Base conventions

- Root ops: `pkexec` not `sudo` — non-interactive shells have no sudo password prompt; pkexec auths via polkit. Example: `pkexec pacman -S --needed <pkg>`.
- Bitbucket SSH: `~/.ssh/id_ed25519_bitbucket` + `~/.ssh/config` with `Host bitbucket.org ssh.bitbucket.org` (Bitbucket moved SSH traffic to `ssh.bitbucket.org`); host keys via `ssh-keyscan -t ed25519,ecdsa,rsa bitbucket.org ssh.bitbucket.org >> ~/.ssh/known_hosts`.
- Home folder is a git repo of `git@ssh.bitbucket.org:galmost/gcachydeck_home.git` with daily user-timer snapshot — see [home-git-snapshot/](home-git-snapshot/README.md).

## 2. Installed set (verified on this box)

| Component | Note | Verified |
|---|---|---|
| zsh login shell + OMZ + p10k + plugins (autosuggestions, syntax-highlighting, web-search) | [../linux/zsh/](../linux/zsh/README.md), [../arch/zsh/](../arch/zsh/README.md) | zsh default shell, `ZSH_THEME="powerlevel10k/powerlevel10k"`; run `p10k configure` once interactively |
| Zed editor + shared config from `ide/zed/` | [../linux/zed/](../linux/zed/README.md), [../arch/zed/](../arch/zed/README.md) | Zed 1.30.2 via `curl -fsSL https://zed.dev/install.sh | sh`, vulkan-radeon, `settings.json` + `keymap.json` copied to `~/.config/zed/` |
| Brave (default browser) | [../linux/brave/](../linux/brave/README.md), [../arch/brave/](../arch/brave/README.md) | Brave 158.1.100.59, `xdg-settings set default-web-browser brave-browser.desktop` |
| udiskie automount tray | [../arch/drives/udiskie/](../arch/drives/udiskie/README.md) | `~/.config/udiskie/config.yml` (automount off, nosuid/nodev/noexec), autostart `~/.config/autostart/udiskie.desktop` |
| CLI tools: htop ncdu aria2 + bat alias | [../debian/cli-tools/](../debian/cli-tools/README.md), [../debian/aria2c/](../debian/aria2c/README.md) | htop 3.5.3, ncdu 2.9.2, aria2 1.37.0 via pacman; rg fd jq fzf bat eza duf preinstalled; `alias batcat="bat"` in `~/.zshrc` (Arch binary is `bat`) |
| wl-clipboard (Wayland clipboard) | — | wl-clipboard 2.3.0 (`wl-copy`/`wl-paste`) |
| GitHub CLI `gh` | — | gh 2.105.0, authed via keyring |
| pi coding agent + caveman skill | [../linux/ai/pi/skills/caveman/](../linux/ai/pi/skills/caveman/README.md) | `pi install git:github.com/v2nic/pi-caveman` |
| Daily home git snapshot | [home-git-snapshot/](home-git-snapshot/README.md) | `gcachydeck-home-snapshot.timer` active, pushes to Bitbucket main |
| KeePassXC + Brave integration | [keepassxc/](keepassxc/README.md) | 2.8.0, `[Browser] Enabled=true`, KeePassXC-Browser ext in Brave |
| Brave debloat + dark mode | [brave-config/](brave-config/README.md) | dark (`color_scheme2=2`), rewards/wallet/leo/news/vpn/sidebar off |
| Digi Storage client | [digistorage/](digistorage/README.md) | `~/.digistorage-dist/storagegui`, desktop + autostart entries |

## 3. Why a cachyos section

Repo rule: notes match distro in path. CachyOS-specific state (own home repo
`gcachydeck_home`, pacman package dumps, pkexec convention on this box) goes
under `computer/cachyos/`; anything generic to Arch stays in `computer/arch/`.

## Source

- CachyOS: https://cachyos.org (Arch-based, rolling)
- Arch notes reused: `computer/arch/`, shared: `computer/linux/`
