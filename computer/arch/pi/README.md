# Pi Coding Agent Setup (CachyOS / Arch Linux)

Install Pi coding agent via npm on Arch-based systems (CachyOS, Arch Linux, Manjaro). Generic Linux: [Pi Coding Agent Setup for Linux](../../linux/pi/).

## 1. Prerequisites

Node.js 18+ and npm. Arch ships both in the AUR (`nodejs` package includes npm; no separate `npm` package — AUR `npm` conflicts):

```bash
sudo pacman -S curl      # only if the AUR helper needs it

yay -S nodejs       # or: paru -S nodejs
node -v
npm -v
```

Do not use the NodeSource setup script here — it targets Debian/Ubuntu.

## 2. Install, update, uninstall

```bash
npm install -g @earendil-works/pi-coding-agent   # add --ignore-scripts to skip post-install scripts
pi --version

npm update -g @earendil-works/pi-coding-agent    # update
npm uninstall -g @earendil-works/pi-coding-agent # uninstall
```

`--ignore-scripts` is safe for upgrades. Use it when post-install scripts fail, when you want to skip optional setup, or while debugging an install; most Pi functionality works without them, though some optional integrations may need manual setup.

## 3. Verify

```bash
pi --version
pi --help
pi                # interactive session
```

## 4. Troubleshooting

### EACCES permission errors

Global installs write `/usr/lib/node_modules` as root. Chowning that dir leaves mixed ownership on next upgrade — avoid. Instead:

```bash
# Option 1: sudo
sudo npm install -g @earendil-works/pi-coding-agent

# Option 2: user prefix
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Option 3: nvm (multi-version Node.js)
nvm install --lts
nvm use --lts
```

Or user-local install without touching npm config: `npm install -g --prefix ~/.local @earendil-works/pi-coding-agent`.

### Node.js too old

Pi needs Node.js 18+. `node -v`; upgrade with `yay -S nodejs`.

### npm not found

`nodejs` AUR package ships npm — reinstall with `yay -S nodejs`. Do not install AUR `npm` alongside.

## 5. Configuration

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

First run: `pi`, or `pi --model mistral-medium-latest`; `pi models` lists models.

## 6. See Also

- [Pi Caveman Setup](../../linux/pi/caveman/) — caveman voice integration
- [Pi Caveman CLI Assessment](../../linux/pi/caveman/cli/) — CLI vs Skills comparison

## Source

- [Pi Coding Agent](https://github.com/earendil-works/pi-coding-agent)
- [Pi Documentation](https://github.com/earendil-works/pi-coding-agent/tree/main/docs)
- [Arch Wiki - Node.js](https://wiki.archlinux.org/title/Node.js)
