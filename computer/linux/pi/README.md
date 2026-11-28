# Pi Coding Agent Setup (Linux)

Pi coding agent harness, works with any provider. Distro-specific notes: [Arch/CachyOS](../../arch/pi/) · [Debian with Mistral + local models](../../debian/ai/pi/).

## 1. Prerequisites

Node.js 18+ (LTS) with npm, plus git for some features.

**Debian/Ubuntu (NodeSource):**

```bash
sudo apt update && sudo apt install -y curl
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs      # npm included
```

**Fedora/RHEL/CentOS:**

```bash
sudo dnf module enable nodejs:20 && sudo dnf install -y nodejs
```

**openSUSE:**

```bash
sudo zypper install -y nodejs20
```

**Arch/Manjaro/CachyOS:** `yay -S nodejs` (AUR `nodejs` includes npm). Details: [Arch guide](../../arch/pi/).

```bash
node -v && npm -v
```

## 2. Install, update, uninstall

```bash
npm install -g @earendil-works/pi-coding-agent    # add --ignore-scripts to skip post-install scripts
pi --version

npm update -g @earendil-works/pi-coding-agent     # update
npm uninstall -g @earendil-works/pi-coding-agent  # uninstall
```

## 3. First run

```bash
pi                                    # interactive session
pi --model gpt-4o-mini                # specific model
pi models                             # list models
pi --help
```

## 4. Configuration

`~/.pi/agent/settings.json`:

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

| Provider | Example models |
|----------|----------------|
| mistral | mistral-medium-latest, mistral-small-latest |
| openai | gpt-4o-mini, gpt-4o |
| anthropic | claude-3-5-sonnet-20250620, claude-3-haiku-20240307 |
| google | gemini-1.5-flash, gemini-1.5-pro |

For OAuth-based providers prefer `pi auth login <provider>`; provider state lands in `~/.pi/agent/auth.json`.

## 5. Troubleshooting

### EACCES permission errors

Global installs need root under `/usr/lib/node_modules`. Never chown that dir (mixed ownership breaks next upgrade). Options: `sudo npm install -g ...`, or a user prefix:

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

Or `npm install -g --prefix ~/.local`, or nvm (`nvm install --lts`).

### Node.js too old / npm missing

`node -v` prints the version; npm ships inside the distro `nodejs` package from NodeSource or the AUR. Reinstall `nodejs`; do not add a separate `npm` package where it conflicts.

### `pi` command not found

```bash
npm config get prefix        # <prefix>/bin must be on PATH
echo 'export PATH=$(npm config get prefix)/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

## See Also

- [Pi Caveman Setup](caveman/) — caveman voice integration
- [Pi Caveman CLI Assessment](caveman/cli/) — CLI vs Skills comparison
- [Arch-specific Pi Setup](../../arch/pi/)

## Source

- [Pi Coding Agent](https://github.com/earendil-works/pi-coding-agent)
- [Pi Documentation](https://github.com/earendil-works/pi-coding-agent/tree/main/docs)
- [NodeSource distributions](https://github.com/nodesource/distributions)
