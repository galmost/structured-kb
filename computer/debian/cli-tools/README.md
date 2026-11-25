# CLI Tools Install (Debian 13)

Tools for terminal. ripgrep fd jq fzf bat eza htop ncdu duf git curl python3 node.

## 1. Prerequisites

```bash
pkexec apt update
```

Use `pkexec` not `sudo` when no interactive. polkit auth. no password ask.

## 2. Install from apt

```bash
pkexec apt install -y fzf bat eza htop ncdu
```

`rg` `fd` maybe already in `~/.pi/agent/bin/`. fallback: `pkexec apt install -y ripgrep fd-find`. Debian `bat` name is `batcat`.

## 3. Install duf (not in Debian repos)

Only `.apk` `.deb` `.rpm` exist. no tarball. no-root: extract deb to `~/.local/bin`:

```bash
cd /tmp
curl -sL -o duf.deb https://github.com/muesli/duf/releases/download/v0.9.1/duf_0.9.1_linux_amd64.deb
dpkg-deb -x duf.deb duf-extract
install -m 755 duf-extract/usr/bin/duf ~/.local/bin/duf
rm -rf duf.deb duf-extract
```

Root way: `pkexec dpkg -i duf.deb`.

`dust` not in trixie. `ncdu` do disk usage.

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

Test:

```bash
rg -l AGENTS.md --glob '*.md' ~/.pi/agent
echo '{"a":1}' | jq .a
fd AGENTS ~/.pi/agent
echo hi | batcat --paging=never
eza -1 ~
```

## 5. Tested

Debian 13 trixie. real run. installed: fzf 0.60, bat 0.25.0 (`batcat`), eza, htop 3.4.1, ncdu 1.22 via apt. duf 0.9.1 via deb extract. rg 15.2.0 fd 10.5.2 in `~/.pi/agent/bin/`.

## Troubleshooting

### pkexec: "Request dismissed"

No polkit agent. non-interactive. use no-root deb extract from section 3. or run from desktop terminal.

### duf release download is not gzip

duf give `.apk` `.deb` `.rpm`. no `.tar.gz`. `.tar.gz` URL give HTML error. use `.deb` and `dpkg-deb -x`.

## Source

- https://github.com/muesli/duf/releases
- https://packages.debian.org/trixie/