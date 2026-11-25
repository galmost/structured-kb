# Zsh Install (Debian / Ubuntu)

## 1. Install Zsh

```bash
pkexec apt install -y zsh
```

## 2. Set as default shell

```bash
chsh -s $(which zsh)
```

Log out. Log in. Changes work. Want bash back:

```bash
chsh -s /usr/bin/bash
```

### Non-interactive shells

Plain `chsh` ask password. Fail no TTY (`chsh: PAM: Authentication failure`). In script/agent run as root. No password needed:

```bash
pkexec usermod -s /usr/bin/zsh "$USER"
```

Check with `grep "$USER" /etc/passwd` — last field must be `/usr/bin/zsh`.

## 3. Shared shell config (Oh My Zsh + Powerlevel10k)

Install shell only step one. Shared OMZ + Powerlevel10k + plugins setup in [computer/linux/zsh/README.md](../../linux/zsh/README.md). Applies all Linux. Debian full sequence:

```bash
pkexec apt install -y zsh
pkexec usermod -s /usr/bin/zsh "$USER"
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" --unattended
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/powerlevel10k
git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

Then in `~/.zshrc` set `ZSH_THEME="powerlevel10k/powerlevel10k"` and `plugins=(git zsh-autosuggestions zsh-syntax-highlighting web-search)`. Run `p10k configure` once in interactive zsh to make `~/.p10k.zsh`.

Gotcha: OMZ installer replace old `~/.zshrc`, move to `~/.zshrc.pre-oh-my-zsh`. If old file had custom lines (e.g. `. "$HOME/.local/bin/env"` for `~/.local/bin` on PATH), add back to new `~/.zshrc` or lost. `--unattended` stop installer touch login shell, so set shell first.

Verified Debian 13 (trixie): zsh 5.9-8+b24, login shell `/usr/bin/zsh`, `.zshrc` passes `zsh -n`.

## Source

- Zsh: https://www.zsh.org/
- Shared OMZ/p10k note: [computer/linux/zsh/README.md](../../linux/zsh/README.md)