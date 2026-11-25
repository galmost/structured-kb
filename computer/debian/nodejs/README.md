# Node.js Setup (NodeSource, Debian 13 / Ubuntu 24.04+)

Install current Node.js LTS from NodeSource apt repo, not distro archive. Distro packages have old runtimes (Debian 13 has Node 20, no support) and split npm into many small packages. NodeSource ships one current `nodejs` package with matching npm. Adapted from [ComputingForGeeks](https://computingforgeeks.com/install-nodejs-ubuntu-debian/).

## 1. Prerequisites

Ubuntu server images already have all. Minimal Debian 13 install maybe not — as root:

```bash
apt install -y sudo curl vim
usermod -aG sudo <username>   # then log in again
```

## 2. Add the NodeSource repository

Download setup script and read before run — it runs as root and edits apt config:

```bash
curl -fsSL https://deb.nodesource.com/setup_24.x -o nodesource_setup.sh
less nodesource_setup.sh        # verify what it does
sudo -E bash nodesource_setup.sh
```

For Node.js 26 instead, use `setup_26.x`. Nothing else change.

Script writes:

- `/usr/share/keyrings/nodesource.gpg` — signing key
- `/etc/apt/sources.list.d/nodesource.sources` — repo (`Suite: nodistro`, serves every Ubuntu/Debian release)
- `/etc/apt/preferences.d/nodejs` — apt pin, priority 600, apt pick NodeSource build over archive even when archive version string sort higher

## 3. Install

npm bundled inside `nodejs` package — do not add separate `npm` package (it conflict):

```bash
sudo apt-get install -y nodejs
node -v
npm -v
npx -v
```

## 4. Build tools for native modules

Packages like `bcrypt`, `sharp` and `better-sqlite3` compile C++ when no prebuilt binary match your platform:

```bash
sudo apt install -y build-essential
```

## Troubleshooting

- `nodejs : Conflicts: npm` — archive's `npm` package already installed, or script tried install it. Nothing broken: npm ships inside NodeSource `nodejs` package. Remove distro `npm` package and drop `npm` from any `apt-get install` line.
- Global installs fail with `EACCES` — `/usr/lib/node_modules` root-owned. Use `sudo npm install -g <pkg>` for machine-wide tools. Never fix by chowning `/usr/lib/node_modules`: next upgrade runs as root again and leaves mixed-ownership directory.
- To pin tooling to user instead, use [nvm](https://github.com/nvm-sh/nvm) — per-user global packages, no sudo.

## Source

- [Install Node.js Ubuntu Debian — ComputingForGeeks](https://computingforgeeks.com/install-nodejs-ubuntu-debian/)