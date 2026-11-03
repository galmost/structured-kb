# Zsh with Powerlevel10k (Linux)

Zsh is a powerful shell that provides enhanced features over bash, including
better tab completion, plugin support, and theming capabilities.
Powerlevel10k is a fast and flexible prompt theme that provides a beautiful,
informative, and customizable spaceship-style prompt.

## 1. Install Zsh

### Debian / Ubuntu

```bash
pkexec apt install -y zsh
```

### Arch Linux

```bash
sudo pacman -S zsh
```

## 2. Set as default shell

```bash
chsh -s $(which zsh)
```

Log out and log back in for changes to take effect. To revert to bash:

```bash
chsh -s /usr/bin/bash
```

## 3. Powerlevel10k Setup

Install Oh My Zsh and Powerlevel10k for a beautiful spaceship-style prompt.

### Install Oh My Zsh

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Do NOT let it change default shell if already done in step 2.

### Install Powerlevel10k theme

```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/powerlevel10k
```

### Set Powerlevel10k as theme

```bash
echo 'ZSH_THEME="powerlevel10k/powerlevel10k"' >> ~/.zshrc
```

## 4. Configure Powerlevel10k

After installation, Powerlevel10k will guide you through an interactive setup:

```bash
source ~/.zshrc
p10k configure
```

Follow the interactive prompts to customize your prompt.

## 5. Recommended Plugins

Enhance your Zsh experience with these useful plugins. Edit `~/.zshrc`:

```bash
nano ~/.zshrc
```

Add these plugins to the plugins array:

```zsh
plugins=(
  git
  zsh-autosuggestions
  zsh-syntax-highlighting
  web-search
)
```

Install additional plugins:

```bash
# Syntax highlighting
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# Autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

## 6. Configuration Files

| File | Purpose |
|------|---------|
| `~/.zshrc` | Main Zsh configuration |
| `~/.p10k.zsh` | Powerlevel10k prompt settings |
| `~/.oh-my-zsh/` | Oh My Zsh framework files |

## Performance Tips

Powerlevel10k is optimized for speed and works well even with many plugins.
Use `hyperfine` to benchmark your shell startup time:

```bash
hyperfine --warmup 3 'zsh -i -c exit'
```

## Official Documentation

- Zsh: https://www.zsh.org/
- Oh My Zsh: https://ohmyz.sh/
- Powerlevel10k: https://github.com/romkatv/powerlevel10k

## Notes

- After changing your default shell, log out and log back in for changes to take effect.
- Powerlevel10k provides interactive configuration on first run (`p10k configure`).
- Customize your prompt style, colors, and information display through the interactive setup.
- Zsh plugins can significantly enhance your productivity with better autocomplete and suggestions.
