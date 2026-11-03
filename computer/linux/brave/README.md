# Brave Browser Setup (Linux)

Installs Brave Browser on Linux. Brave is a privacy-focused Chromium-based
browser with built-in ad blocking, Tor support, and reward system.

## 1. Debian / Ubuntu

### 1.1 Prerequisites

```bash
pkexec apt install -y curl gnupg
```

### 1.2 Add Brave repository

```bash
curl -fsSL https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg | pkexec gpg --dearmor -o /usr/share/keyrings/brave-browser-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | pkexec tee /etc/apt/sources.list.d/brave-browser-release.list
```

### 1.3 Install

```bash
pkexec apt update
pkexec apt install -y brave-browser
```

## 2. Distro specific

### 2.1 Debian

```bash
# Add keyring
curl -fsSL https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg | pkexec gpg --dearmor -o /usr/share/keyrings/brave-browser-archive-keyring.gpg

# Add repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | pkexec tee /etc/apt/sources.list.d/brave-browser-release.list

# Update and install
pkexec apt update
pkexec apt install -y brave-browser

# Result
brave-browser --version   # Brave Browser 156.1.98.63
```


### 2.2 Arch Linux - Install from AUR

Brave is in AUR as `brave-bin`. Use your preferred AUR helper:

```bash
yay -S brave-bin
# or
paru -S brave-bin
# or manually
git clone https://aur.archlinux.org/brave-bin.git
cd brave-bin
makepkg -si
```

### 2.2 Verify

```bash
brave --version
```

## Troubleshooting

### Debian: Repository errors

`404 Not Found` — check the repository URL is correct. Brave changed from
`brave.com` to `brave-browser-apt-release.s3.brave.com` hosting.

### Arch: Build fails

Missing dependencies — install `base-devel` and `git`.
`makepkg -si` fails with signature error — run `gpg --recv-keys <key-id>`
from the PKGBUILD or use `--skip-integrity-checks` as last resort.

### Both: Brave not launching

Check desktop environment integration:
```bash
update-desktop-database -q
```

### Both: Sandbox issues

Brave uses Chromium sandbox. If crashes, try disabling:
```bash
brave-browser --no-sandbox
```
Not recommended for security. Fix proper kernel/user namespace support instead.

## Source

- [Brave Linux installation guide](https://brave.com/linux/)
- [Brave AUR package](https://aur.archlinux.org/packages/brave-bin)
