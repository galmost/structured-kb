# Zsh Install (Debian / Ubuntu)

## 1. Install Zsh

```bash
pkexec apt install -y zsh
```

## 2. Set as default shell

```bash
chsh -s $(which zsh)
```

Log out and log back in for changes to take effect. To revert to bash:

```bash
chsh -s /usr/bin/bash
```

### Non-interactive shells

Plain `chsh` prompts for a password through PAM and fails without a TTY
(`chsh: PAM: Authentication failure`). In scripts or agent sessions run it
as root instead, which needs no password:

```bash
pkexec usermod -s /usr/bin/zsh "$USER"
```

Verify with `grep "$USER" /etc/passwd` — the last field must be
`/usr/bin/zsh`.

## 3. Shared shell config (Oh My Zsh + Powerlevel10k)

Installing the shell is only step one. The shared OMZ + Powerlevel10k +
plugins setup lives in [computer/linux/zsh/README.md](../../linux/zsh/README.md)
and applies to every Linux distro. On Debian the full sequence is:

```bash
pkexec apt install -y zsh
pkexec usermod -s /usr/bin/zsh "$USER"
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" --unattended
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/powerlevel10k
git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

Then in `~/.zshrc` set `ZSH_THEME="powerlevel10k/powerlevel10k"` and
`plugins=(git zsh-autosuggestions zsh-syntax-highlighting web-search)`.
Run `p10k configure` once in an interactive zsh to generate `~/.p10k.zsh`.

Gotcha: the OMZ installer replaces an existing `~/.zshrc` and moves it to
`~/.zshrc.pre-oh-my-zsh`. If the old file had custom lines (e.g.
`. "$HOME/.local/bin/env"` for `~/.local/bin` on PATH), re-append them to
the new `~/.zshrc` or they are lost. `--unattended` keeps the installer
from touching the login shell, so set the shell first.

Verified on Debian 13 (trixie): zsh 5.9-8+b24, login shell `/usr/bin/zsh`,
`.zshrc` passes `zsh -n`.

## Source

- Zsh: https://www.zsh.org/
- Shared OMZ/p10k note: [computer/linux/zsh/README.md](../../linux/zsh/README.md)
