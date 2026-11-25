# CLI Tools Install (Debian 13)

Daily-driver terminal tools for agent and interactive use: ripgrep, fd,
jq, fzf, bat, eza, htop, ncdu, duf, plus git/curl/python3/node base.

## 1. Prerequisites

```bash
pkexec apt update
```

In non-interactive shells prefer `pkexec` over `sudo` (polkit auth, no
password prompt).

## 2. Install from apt

```bash
pkexec apt install -y fzf bat eza htop ncdu
```

`rg` and `fd` may already ship in the agent PATH (e.g. `~/.pi/agent/bin/`);
apt copies exist as fallback: `pkexec apt install -y ripgrep fd-find`.
On Debian the `bat` binary is named `batcat`.

## 3. Install duf (not in Debian repos)

Only `.apk`/`.deb`/`.rpm` assets are published, no plain tarball.
No-root path — extract the deb into `~/.local/bin`:

```bash
cd /tmp
curl -sL -o duf.deb https://github.com/muesli/duf/releases/download/v0.9.1/duf_0.9.1_linux_amd64.deb
dpkg-deb -x duf.deb duf-extract
install -m 755 duf-extract/usr/bin/duf ~/.local/bin/duf
rm -rf duf.deb duf-extract
```

Root alternative: `pkexec dpkg -i duf.deb`.

`dust` is also absent from trixie repos; `ncdu` covers disk usage.

## 4. Verify

```bash
rg --version        # ripgrep 15.2.0
fd --version        # fd 10.5.2
jq --version
fzf --version       # 0.60
batcat --version    # bat 0.25.0
eza --version
htop --version      # htop 3.4.1
ncdu --version      # ncdu 1.22
duf --version       # duf 0.9.1
```

Smoke tests:

```bash
rg -l AGENTS.md --glob '*.md' ~/.pi/agent
echo '{"a":1}' | jq .a
fd AGENTS ~/.pi/agent
echo hi | batcat --paging=never
eza -1 ~
```

## 5. Tested

Debian 13 (trixie), commands run for real. Installed: fzf 0.60, bat 0.25.0
(`batcat`), eza, htop 3.4.1, ncdu 1.22 via apt; duf 0.9.1 via deb extract.
rg 15.2.0 and fd 10.5.2 already present in `~/.pi/agent/bin/`.

## Troubleshooting

### pkexec: "Request dismissed"

No polkit agent in the current shell (non-interactive session). Use the
no-root deb-extract path from section 3, or run pkexec from a desktop
terminal.

### duf release download is not gzip

duf publishes `.apk`/`.deb`/`.rpm`, not `.tar.gz`. A `.tar.gz` URL
returns an HTML error page; use the `.deb` asset and `dpkg-deb -x`.

## Source

- https://github.com/muesli/duf/releases
- https://packages.debian.org/trixie/
