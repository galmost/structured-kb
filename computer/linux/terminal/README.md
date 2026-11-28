# Terminal Capabilities (Linux, Konsole/Wayland)

Terminal capabilities test + setup for CachyOS/Arch with Konsole on Wayland. Covers colors, clipboard, images, notifications, fonts.

## 1. Detected Environment

| Property | Value |
|----------|-------|
| Terminal | Konsole 26.08.3 |
| Session | Wayland (`XDG_SESSION_TYPE=wayland`, `WAYLAND_DISPLAY=wayland-1`) |
| TERM | `xterm-256color` |
| COLORTERM | `truecolor` |
| Colors | 256 |
| Shell | fish 4.9.3 (login), bash in pi |
| Locale | `en_US.UTF-8` |
| Fonts | MesloLGS Nerd Font (bold/italic/regular) |

## 2. ANSI/Color Capabilities (tput)

| Capability | Status | Escape |
|------------|--------|--------|
| bold | ✅ | `^[[1m` |
| dim | ✅ | `^[[2m` |
| underline | ✅ | `^[[4m` |
| blink | ✅ | `^[[5m` |
| reverse | ✅ | `^[[7m` |
| 256 colors | ✅ | `tput colors` → 256 |
| truecolor | ✅ | `COLORTERM=truecolor` |
| UTF-8 glyphs | ✅ | ✓ ✗ ● → █ ▓ etc. render |

Test:

```bash
tput colors && tput bold && echo "bold OK" && tput sgr0
printf "✓ ✗ → █ ▓ ⭐ ✅\n"
```

## 3. Clipboard Tools

| Tool | Protocol | Status | Install |
|------|----------|--------|---------|
| `wl-copy`/`wl-paste` | Wayland | ✅ wl-clipboard 2.3.0 | `pacman -S wl-clipboard` |
| `xclip` | X11/XWayland | ✅ installed | `pkexec pacman -S xclip` |
| `xsel` | X11/XWayland | ✅ installed | `pkexec pacman -S xsel` |

Usage:

```bash
echo "text" | wl-copy          # Wayland native
wl-paste                       # paste
echo "text" | xclip -selection clipboard   # XWayland
xclip -selection clipboard -o             # paste
```

## 4. Image Rendering in Terminal

| Tool | Status | Install | Notes |
|------|--------|---------|-------|
| `chafa` | ✅ 1.18.3 | `pkexec pacman -S chafa` | Best terminal image renderer |
| `img2txt` | ✅ (caca-utils) | preinstalled | ASCII art fallback |
| `viu` | ❌ | AUR `viu` | Rust image viewer, optional |

Usage:

```bash
chafa image.png              # render image
chafa -s 80x24 image.png     # size to terminal
img2txt image.png            # ASCII fallback
```

## 5. Notifications

| Tool | Status | Install |
|------|--------|---------|
| `notify-send` | ✅ | `pacman -S libnotify` |

Usage:

```bash
notify-send "Title" "Message"
notify-send -u critical "Alert" "Something important"
```

## 6. Install Missing Tools

```bash
# X11 clipboard for XWayland apps + chafa for images
pkexec pacman -S --needed --noconfirm xclip xsel chafa

# Optional: viu (AUR, Rust image viewer)
yay -S viu
```

## 7. Verify

```bash
# Colors
echo -e "\e[1;31mRED BOLD\e[0m \e[4mUNDERLINE\e[0m \e[256m256color\e[0m"

# Clipboard
echo "test" | wl-copy && wl-paste
echo "test" | xclip -selection clipboard && xclip -selection clipboard -o

# Image
chafa --version

# Notify
notify-send "Test" "Notification works"

# Glyphs
printf "Nerd Font: \uf013 \uf07b \uf121 \uf0e7\n"
```

## 8. Troubleshooting

- `xclip` hangs on Wayland — use `wl-copy` instead for native Wayland apps
- `chafa` shows garbage — terminal may not support it; use `img2txt`
- Colors look wrong — check `COLORTERM=truecolor` is set
- Nerd Font glyphs show as boxes — install `ttf-meslo-nerd-fonts` or `awesome-terminal-fonts`

## Source

- [Konsole](https://konsole.kde.org/)
- [wl-clipboard](https://github.com/bugaevc/wl-clipboard)
- [chafa](https://hpjansson.org/chafa/)
- [Nerd Fonts](https://www.nerdfonts.com/)
