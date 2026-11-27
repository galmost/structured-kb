# Pi Coding Agent Setup (Linux)

Install and configure Pi coding agent on Linux distributions. Pi is a coding agent harness that works with various LLMs.

## 1. Prerequisites

- Node.js 18+ (LTS recommended)
- npm (bundled with Node.js)
- Git (optional, for some features)

### Install Node.js

**Debian/Ubuntu (via NodeSource):**

```bash
# Install prerequisites
sudo apt update
sudo apt install -y curl

# Add NodeSource repository (adjust version as needed)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

# Install Node.js (includes npm)
sudo apt install -y nodejs

# Verify
node -v
npm -v
```

**Fedora/RHEL/CentOS:**

```bash
# Install Node.js from AppStream or third-party repo
sudo dnf module enable nodejs:20
sudo dnf install -y nodejs

# Or from NodeSource
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo dnf install -y nodejs

# Verify
node -v
npm -v
```

**OpenSUSE:**

```bash
# Install Node.js
sudo zypper install -y nodejs20

# Or from NodeSource
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo zypper install -y nodejs

# Verify
node -v
npm -v
```

**Arch/Manjaro/CachyOS:**

```bash
# Install from AUR
yay -S nodejs npm
# or
paru -S nodejs npm

# Verify
node -v
npm -v
```

## 2. Install Pi

```bash
# Global install (recommended)
npm install -g @earendil-works/pi-coding-agent

# Verify installation
pi --version
```

### With --ignore-scripts Flag

Skip post-install scripts (safe for most use cases):

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

**Use cases:**
- Post-install scripts failing
- Debugging installation
- Minimal setup

## 3. Verify Installation

```bash
# Check version
pi --version

# List commands
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
```

## 5. Uninstall Pi

```bash
npm uninstall -g @earendil-works/pi-coding-agent
```

## 6. Configuration

Pi configuration file: `~/.pi/agent/settings.json`

### Basic Configuration

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

### Common Providers

| Provider | Models |
|----------|--------|
| mistral | mistral-medium-latest, mistral-small-latest, mistral-tiny-latest |
| openai | gpt-4o-mini, gpt-4o, gpt-3.5-turbo |
| anthropic | claude-3-5-sonnet-20250620, claude-3-haiku-20240307 |
| google | gemini-1.5-flash, gemini-1.5-pro |

### Set Default Provider

```bash
# Edit settings
nano ~/.pi/agent/settings.json
```

Update `defaultProvider` and `defaultModel`:

```json
{
  "defaultProvider": "openai",
  "defaultModel": "gpt-4o-mini"
}
```

## 7. API Keys

Set API keys for your providers:

```bash
# Create or edit environment file
nano ~/.pi/agent/auth.json
```

Example:

```json
{
  "openai": {
    "apiKey": "sk-..."
  },
  "anthropic": {
    "apiKey": "sk_ant_..."
  },
  "mistral": {
    "apiKey": "..."
  }
}
```

**Note**: Keep API keys secure. Use file permissions:

```bash
chmod 600 ~/.pi/agent/auth.json
```

## 8. First Run

```bash
# Start Pi
pi

# Or with specific model
pi --model gpt-4o-mini

# List available models
pi models
```

## 9. Common Commands

| Command | Description |
|---------|-------------|
| `pi` | Start interactive session |
| `pi --model <model>` | Start with specific model |
| `pi --provider <provider>` | Start with specific provider |
| `pi models` | List available models |
| `pi --help` | Show help |
| `pi --version` | Show version |

## 10. Platform-Specific Notes

### Debian/Ubuntu

- NodeSource recommended for current Node.js
- Distro packages may be outdated
- Use `sudo` for global installs or change npm prefix

### Fedora/RHEL

- Use NodeSource or AppStream modules
- AppStream may have older versions

### Arch/Manjaro/CachyOS

- Use AUR (`nodejs` package includes npm)
- See [Arch-specific guide](../../arch/pi/) for details

### OpenSUSE

- Use NodeSource or OBS repositories
- OBS may have older versions

## 11. Troubleshooting

### EACCES Permission Errors

Global npm installs require root for `/usr/lib/node_modules`:

```bash
# Option 1: Use sudo
sudo npm install -g @earendil-works/pi-coding-agent

# Option 2: Change npm prefix
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g @earendil-works/pi-coding-agent

# Option 3: Use nvm
nvm install --lts
nvm use --lts
npm install -g @earendil-works/pi-coding-agent
```

### Node.js Version Too Old

Pi requires Node.js 18+:

```bash
# Check version
node -v

# If < 18, upgrade Node.js
# Debian/Ubuntu: use NodeSource (see above)
# Fedora/RHEL: use NodeSource or AppStream
# Arch: yay -S nodejs
```

### npm Not Found

If npm missing:

```bash
# Debian/Ubuntu: npm included in nodejs package from NodeSource
# Fedora/RHEL: npm included in nodejs package
# Arch: npm included in nodejs AUR package

# Reinstall Node.js if npm missing
```

### Pi Command Not Found

```bash
# Check npm global prefix
npm config get prefix

# Add to PATH if not already there
echo 'export PATH=$(npm config get prefix)/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

## 12. See Also

- [Pi Caveman Setup](./caveman/) - Caveman voice integration
- [Pi Caveman CLI Assessment](./caveman/cli/) - CLI vs Skills comparison
- [Arch-specific Pi Setup](../../arch/pi/) - Arch Linux/CachyOS guide

## Source

- [Pi Coding Agent](https://github.com/earendil-works/pi-coding-agent)
- [Pi Documentation](https://github.com/earendil-works/pi-coding-agent/tree/main/docs)
- [NodeSource](https://github.com/nodesource/distributions)
