# Node.js Setup (NodeSource, Debian 13 / Ubuntu 24.04+)

Installs the current Node.js LTS from NodeSource's apt repository instead of
the distro archive. Distro packages ship outdated runtimes (Debian 13 has
Node 20, out of support) and split npm into hundreds of small packages;
NodeSource ships one current `nodejs` package with matching npm. Adapted from
[ComputingForGeeks](https://computingforgeeks.com/install-nodejs-ubuntu-debian/).

## 1. Prerequisites

Ubuntu server images already have everything. A minimal Debian 13 install
may not — as root:

```bash
apt install -y sudo curl vim
usermod -aG sudo <username>   # then log in again
```

## 2. Add the NodeSource repository

Download the setup script and read it before running — it runs as root and
edits apt configuration:

```bash
curl -fsSL https://deb.nodesource.com/setup_24.x -o nodesource_setup.sh
less nodesource_setup.sh        # verify what it does
sudo -E bash nodesource_setup.sh
```

For Node.js 26 instead, use `setup_26.x`. Nothing else changes.

The script writes:

- `/usr/share/keyrings/nodesource.gpg` — signing key
- `/etc/apt/sources.list.d/nodesource.sources` — repository (`Suite: nodistro`, serves every Ubuntu/Debian release)
- `/etc/apt/preferences.d/nodejs` — apt pin, priority 600, so apt prefers NodeSource's build over the archive even when the archive's version string sorts higher

## 3. Install

npm is bundled inside the `nodejs` package — do not add a separate `npm`
package (it conflicts):

```bash
sudo apt-get install -y nodejs
node -v
npm -v
npx -v
```

## 4. Build tools for native modules

Packages such as `bcrypt`, `sharp` and `better-sqlite3` compile C++ when no
prebuilt binary matches your platform:

```bash
sudo apt install -y build-essential
```

## Troubleshooting

- `nodejs : Conflicts: npm` — the archive's `npm` package was already
  installed, or a script tried to install it. Nothing is broken: npm ships
  inside the NodeSource `nodejs` package. Remove the distro `npm` package
  and drop `npm` from any `apt-get install` line.
- Global installs fail with `EACCES` — `/usr/lib/node_modules` is root-owned.
  Use `sudo npm install -g <pkg>` for machine-wide tools. Never fix it by
  chowning `/usr/lib/node_modules`: the next upgrade runs as root again and
  leaves a mixed-ownership directory.
- To pin the tooling to a user instead, use
  [nvm](https://github.com/nvm-sh/nvm) — per-user global packages, no sudo.

## Source

- [Install Node.js on Ubuntu and Debian — ComputingForGeeks](https://computingforgeeks.com/install-nodejs-ubuntu-debian/)
