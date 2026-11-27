# Pi Coding Agent Setup (CachyOS / Arch Linux)

Install Pi coding agent via npm on Arch-based systems (CachyOS, Arch Linux, Manjaro). For generic Linux setup, see [Pi Coding Agent Setup for Linux](../../linux/pi/).

## 1. Prerequisites

Node.js 18+ and npm required. CachyOS/Arch does not ship Node.js in official repos. Install from AUR or NodeSource.

### Option A: Install Node.js from AUR (Recommended)

```bash
# Install nodejs and npm from AUR
yay -S nodejs npm

# Or with paru
paru -S nodejs npm

# Verify
node -v
npm -v
```

### Option B: Install Node.js from NodeSource

```bash
# Install dependencies
sudo pacman -S curl

# Download and run NodeSource setup (adjust version as needed)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

# Install Node.js (this will also install npm)
sudo pacman -S nodejs

# Verify
node -v
npm -v
```

**Note**: NodeSource is primarily for Debian/Ubuntu. Arch users should prefer AUR (`nodejs` package includes npm).

## 2. Install Pi

```bash
# Global install (recommended)
npm install -g @earendil-works/pi-coding-agent

# Verify
pi --version
```

### With --ignore-scripts flag

Use `--ignore-scripts` to skip post-install scripts (safe for upgrades):

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

**When to use**:
- Post-install scripts failing
- Want to skip optional setup
- Debugging installation issues

**Note**: Most Pi functionality works without post-install scripts. Some optional integrations may require manual setup.

## 3. Verify Installation

```bash
# Check version
pi --version

# List available commands
pi --help

# Start interactive session
pi
```

## 4. Update Pi

```bash
# Update to latest version
npm update -g @earendil-works/pi-coding-agent

# Or reinstall
npm install -g @earendil-works/pi-coding-agent

# With ignore-scripts
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

## 5. Uninstall Pi

```bash
npm uninstall -g @earendil-works/pi-coding-agent
```

## 6. Troubleshooting

### EACCES Permission Errors

Global npm installs require root for `/usr/lib/node_modules`. Solutions:

```bash
# Option 1: Use sudo
sudo npm install -g @earendil-works/pi-coding-agent

# Option 2: Change npm prefix to user directory
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g @earendil-works/pi-coding-agent

# Option 3: Use nvm (recommended for multi-version Node.js)
nvm install --lts
nvm use --lts
npm install -g @earendil-works/pi-coding-agent
```

### Node.js Version Too Old

Pi requires Node.js 18+. Check version:

```bash
node -v
```

If too old, upgrade Node.js:

```bash
# AUR
yay -S nodejs

# Or reinstall from NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo pacman -S nodejs
```

### npm Not Found

If npm missing after Node.js install:

```bash
# AUR nodejs package includes npm - reinstall
ay -S nodejs

# Or install npm separately
ay -S npm
```

## 7. Configuration

Pi configuration stored in `~/.pi/agent/settings.json`. Edit to customize:

```json
{
  "defaultProvider": "mistral",
  "defaultModel": "mistral-medium-latest",
  "packages": [],
  "skills": [],
  "extensions": [],
  "prompts": [],
  "themes": []
}
```

## 8. First Run

```bash
# Start Pi
pi

# Or with specific model
pi --model mistral-medium-latest

# List available models
pi models
```

## 9. See Also

- [Pi Caveman Setup](../linux/pi/caveman/) - Caveman voice integration
- [Pi Caveman CLI Assessment](../linux/pi/caveman/cli/) - CLI vs Skills comparison

## Source

- [Pi Coding Agent](https://github.com/earendil-works/pi-coding-agent)
- [Pi Documentation](https://github.com/earendil-works/pi-coding-agent/tree/main/docs)
- [Arch Wiki - Node.js](https://wiki.archlinux.org/title/Node.js)
