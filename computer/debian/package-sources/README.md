# Package sources and update tracking (Debian 13)

Rule: never drop raw binary in `~/.local/bin` without tracking story.
Like order for installs:

1. `apt` / dpkg — tracked, update with `apt upgrade`. Use when candidate exists (`apt-cache policy <pkg>`).
2. `uv tool` / `uv python` — tracked in uv metadata; update with `uv tool upgrade --all` / `uv python upgrade`.
3. `npm install -g --prefix ~/.local` — update with `npm update -g`.
4. Official self-update installers (zed) — update via app itself.
5. GitHub-release binary last choice — write exact version/commit, upstream URL, and re-download command in topic note, or pin in home_config.

## 1. Audit of `~/.local/bin` (2026-11)

| binary | was | now | update path |
|---|---|---|---|
| `duf` | raw GitHub-release binary 0.9.1, no track | apt `duf 0.8.1-2+b9` at `/usr/bin/duf` (old one kept as `duf.release-bak`) | `apt upgrade` |
| `rg` | pi-bundled binary in `~/.pi/agent/bin` | apt `ripgrep` at `/usr/bin/rg` (pi copy first in PATH, updates with pi via npm) | `apt upgrade` |
| `fd` | pi-bundled binary in `~/.pi/agent/bin` | apt `fd-find` at `/usr/bin/fdfind` (Debian calls `fd` as `fdfind`; pi's `fd` first in PATH) | `apt upgrade` |
| `tmux` | wrapper to source build in `~/.local/usr/bin` | apt `tmux 3.5a-3` at `/usr/bin/tmux` (wrapper kept as `tmux.source-bak`) | `apt upgrade` |
| `pi` | npm global, `~/.local/lib/node_modules` | same | `npm update -g` |
| `uv`, `uvx` | uv binary | same | `uv self update` |
| `vibe`, `vibe-acp`, `vibe-app-server` | `uv tool install mistral-vibe` | same | `uv tool upgrade mistral-vibe` |
| `zed` | official installer, `~/.local/zed.app` | same | self-update |
| `python3.14` | uv-managed CPython | same | `uv python upgrade` |
| `avalon-server`, `gemma-server`, `gemma-31b-server`, `qwen-coder-server`, `qwen38-27b-server` | wrapper scripts around `~/Avalon/build/bin/llama-server` (built from source) | same — no apt equivalent; see [Avalon note](../ai/amd/avalon/README.md) | rebuild from source per that note |

## 2. Fix applied

```bash
pkexec apt-get install -y duf tmux        # dpkg-tracked replacements
mv ~/.local/bin/duf ~/.local/bin/duf.release-bak
mv ~/.local/bin/tmux ~/.local/bin/tmux.source-bak
hash -r; which duf tmux                   # /usr/bin/duf, /usr/bin/tmux
dpkg -S "$(which duf)" "$(which tmux)"     # both owned by dpkg
```

`~/.local/bin` before `/usr/bin` in PATH, so old files moved out of way, not just shadowed.

PATH note: `~/.pi/agent/bin` and `~/.local/bin` before `/usr/bin`, so `which rg` / `which fd` show pi's bundled copies even with apt installed.
Both have tracking story (npm for pi's, dpkg for apt's); don't delete pi's — harness uses them.

Other CLI tools already dpkg-tracked: `fzf`, `jq`, `batcat` (package `bat`),
`eza`, `htop`, `ncdu`, `gh`, `pkexec`. Missing, with apt candidates if ever needed: `bat` (use `batcat`), `btop`, `dust`, `tldr`, `trash-cli`.

## 3. Rule of thumb for new tools

```bash
apt-cache policy <pkg> | grep Candidate   # 1. apt first
# only if absent: uv tool / npm / official installer / pinned release binary
```

When release binary unavoidable, keep download command and version
in topic note and in home_config so next machine (or reinstall) gets same version.

## Source

- https://wiki.debian.org/Apt
- https://docs.astral.sh/uv/ , https://docs.npmjs.com/