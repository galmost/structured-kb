# Zsh Install (Arch Linux)

## 1. Install Zsh

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

## Source

- Zsh: https://www.zsh.org/
