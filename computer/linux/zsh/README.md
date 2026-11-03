# Zsh with Powerlevel10k (Linux)

Zsh is a powerful shell with enhanced tab completion, plugin support, and
theming. Powerlevel10k provides a fast, customizable spaceship-style prompt.

## Install Zsh

Distro-specific install steps:

- Debian / Ubuntu: see [computer/debian/zsh/README.md](../../debian/zsh/README.md)
- Arch: see [computer/arch/zsh/README.md](../../arch/zsh/README.md)

## Set as default shell

```bash
chsh -s $(which zsh)
```

Log out and log back in. To revert to bash:

```bash
chsh -s /usr/bin/bash
```

## Powerlevel10k Setup

### Install Oh My Zsh

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Do NOT let it change default shell if already done above.

### Install Powerlevel10k theme

```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/powerlevel10k
```

### Set theme

```bash
echo 'ZSH_THEME="powerlevel10k/powerlevel10k"' >> ~/.zshrc
```

## Configure Powerlevel10k

```bash
source ~/.zshrc
p10k configure
```

Follow interactive prompts.

## Recommended Plugins

Edit `~/.zshrc`:

```zsh
plugins=(
  git
  zsh-autosuggestions
  zsh-syntax-highlighting
  web-search
)
```

Install:

```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

## Configuration Files

| File | Purpose |
|------|---------|
| `~/.zshrc` | Main Zsh configuration |
| `~/.p10k.zsh` | Powerlevel10k prompt settings |
| `~/.oh-my-zsh/` | Oh My Zsh framework files |

## Performance

Benchmark with hyperfine:

```bash
hyperfine --warmup 3 'zsh -i -c exit'
```

## Source

- Zsh: https://www.zsh.org/
- Oh My Zsh: https://ohmyz.sh/
- Powerlevel10k: https://github.com/romkatv/powerlevel10k
