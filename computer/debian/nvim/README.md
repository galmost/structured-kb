# Neovim Setup (Debian 13)

`nvim` is Vim fork still maintained. Debian 13 (trixie) ship as `neovim` package (NVIM v0.10.4). Install also register `nvim` as system `vim`, `view` and `vimdiff` via `update-alternatives`, so plain `vim` start Neovim.

## 1. Install

```bash
pkexec apt-get update
pkexec apt-get install -y neovim
```

Use `sudo apt-get install -y neovim` instead if passwordless sudo configured. `pkexec` preferred here because `sudo` prompt password in non-interactive shell, while `pkexec` authenticate via polkit.

## 2. Verify

```bash
nvim --version
```

Expected on Debian 13 (trixie): `NVIM v0.10.4`, `LuaJIT 2.1`.

Confirm `vi`/`vim` alternatives now resolve to nvim:

```bash
readlink -f /usr/bin/vi    # /usr/bin/nvim
readlink -f /usr/bin/vim   # /usr/bin/nvim
```

## 3. Pin `vi`/`vim` to nvim

Package register nvim for `vi`, `vim`, `ex`, `view` and `vimdiff` in auto mode, so already point to nvim. Pin them explicit so future package with higher priority cannot steal link:

```bash
pkexec update-alternatives --set vi /usr/bin/nvim
pkexec update-alternatives --set vim /usr/bin/nvim
```

This switch links to manual mode:

```bash
update-alternatives --display vi   # "manual mode ... points to /usr/bin/nvim"
```

## 4. Point `vim` back at real Vim (optional)

If want `vim` stay classic Vim and use `nvim` explicit:

```bash
pkexec update-alternatives --config vim
```

Pick `/usr/bin/vim.basic` entry in interactive list.

## Troubleshooting

### `sudo apt ...` hangs on a password prompt in scripts/terminals without a TTY
Use `pkexec apt ...` instead; it authenticate through polkit and work non-interactively in this session.

### `nvim: command not found` right after install
Shell cached old PATH lookup. Run:

```bash
hash -r
```

or open new shell, then retry `nvim --version`.

### `vim` still starts classic Vim after install
Check which alternative selected:

```bash
update-alternatives --display vim
```

In auto mode highest-priority alternative win; neovim register itself for `vim`, so reinstall with `pkexec apt-get install --reinstall -y neovim` restore it, or switch manual with `pkexec update-alternatives --config vim`.

## Source

- Debian package page: https://packages.debian.org/trixie/neovim
- Neovim docs: https://neovim.io/doc/