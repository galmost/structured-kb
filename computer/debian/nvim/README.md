# Neovim Setup (Debian 13)

Neovim (`nvim`) is the actively maintained Vim fork. Debian 13 (trixie)
ships it as the `neovim` package (NVIM v0.10.4). Installing it also
registers `nvim` as the system `vim`, `view` and `vimdiff` via
`update-alternatives`, so plain `vim` starts Neovim.

## 1. Install

```bash
pkexec apt-get update
pkexec apt-get install -y neovim
```

Use `sudo apt-get install -y neovim` instead if passwordless sudo is
configured. `pkexec` is preferred here because `sudo` prompts for a
password in a non-interactive shell, while `pkexec` authenticates via
polkit.

## 2. Verify

```bash
nvim --version
```

Expected on Debian 13 (trixie): `NVIM v0.10.4`, `LuaJIT 2.1`.

Confirm the `vi`/`vim` alternatives now resolve to nvim:

```bash
readlink -f /usr/bin/vi    # /usr/bin/nvim
readlink -f /usr/bin/vim   # /usr/bin/nvim
```

## 3. Pin `vi`/`vim` to nvim

The package registers nvim for `vi`, `vim`, `ex`, `view` and `vimdiff` in
auto mode, so they already point to nvim. Pin them explicitly so a future
package with higher priority cannot steal the link:

```bash
pkexec update-alternatives --set vi /usr/bin/nvim
pkexec update-alternatives --set vim /usr/bin/nvim
```

This switches the links to manual mode:

```bash
update-alternatives --display vi   # "manual mode ... points to /usr/bin/nvim"
```

## 4. Point `vim` back at real Vim (optional)

If you want `vim` to stay classic Vim and use `nvim` explicitly:

```bash
pkexec update-alternatives --config vim
```

Pick the `/usr/bin/vim.basic` entry in the interactive list.

## Troubleshooting

### `sudo apt ...` hangs on a password prompt in scripts/terminals without a TTY
Use `pkexec apt ...` instead; it authenticates through polkit and works
non-interactively in this session.

### `nvim: command not found` right after install
The shell cached the old PATH lookup. Run:

```bash
hash -r
```

or open a new shell, then retry `nvim --version`.

### `vim` still starts classic Vim after install
Check which alternative is selected:

```bash
update-alternatives --display vim
```

In auto mode the highest-priority alternative wins; neovim registers
itself for `vim`, so reinstalling with `pkexec apt-get install --reinstall -y neovim`
restores it, or switch manually with `pkexec update-alternatives --config vim`.

## Source

- Debian package page: https://packages.debian.org/trixie/neovim
- Neovim docs: https://neovim.io/doc/
