# Package sources and update tracking (Debian 13)

Rule: never drop a raw binary into `~/.local/bin` without a tracking story.
Preference order for installs:

1. `apt` / dpkg — tracked, updated by `apt upgrade`. Use whenever a candidate
   exists (`apt-cache policy <pkg>`).
2. `uv tool` / `uv python` — tracked in uv's metadata; update with
   `uv tool upgrade --all` / `uv python upgrade`.
3. `npm install -g --prefix ~/.local` — update with `npm update -g`.
4. Official self-updating installers (zed) — update via the app itself.
5. GitHub-release binary as last resort — record the exact version/commit,
   the upstream URL, and a re-download command in the topic note, or pin it
   in home_config.

## 1. Audit of `~/.local/bin` (2026-11)

| binary | was | now | update path |
|---|---|---|---|
| `duf` | raw GitHub-release binary 0.9.1, untracked | apt `duf 0.8.1-2+b9` at `/usr/bin/duf` (old one kept as `duf.release-bak`) | `apt upgrade` |
| `rg` | pi-bundled binary in `~/.pi/agent/bin` | apt `ripgrep` at `/usr/bin/rg` (pi's copy stays first in PATH, updates with pi via npm) | `apt upgrade` |
| `fd` | pi-bundled binary in `~/.pi/agent/bin` | apt `fd-find` at `/usr/bin/fdfind` (Debian ships the `fd` name as `fdfind`; pi's `fd` stays first in PATH) | `apt upgrade` |
| `tmux` | wrapper to source build in `~/.local/usr/bin` | apt `tmux 3.5a-3` at `/usr/bin/tmux` (wrapper kept as `tmux.source-bak`) | `apt upgrade` |
| `pi` | npm global, `~/.local/lib/node_modules` | unchanged | `npm update -g` |
| `uv`, `uvx` | uv binary | unchanged | `uv self update` |
| `vibe`, `vibe-acp`, `vibe-app-server` | `uv tool install mistral-vibe` | unchanged | `uv tool upgrade mistral-vibe` |
| `zed` | official installer, `~/.local/zed.app` | unchanged | self-update |
| `python3.14` | uv-managed CPython | unchanged | `uv python upgrade` |
| `avalon-server`, `gemma-server`, `gemma-31b-server`, `qwen-coder-server`, `qwen38-27b-server` | wrapper scripts around `~/Avalon/build/bin/llama-server` (built from source) | unchanged — no apt equivalent; see [Avalon note](../ai/amd/avalon/README.md) | rebuild from source per that note |

## 2. Fix applied

```bash
pkexec apt-get install -y duf tmux        # dpkg-tracked replacements
mv ~/.local/bin/duf ~/.local/bin/duf.release-bak
mv ~/.local/bin/tmux ~/.local/bin/tmux.source-bak
hash -r; which duf tmux                   # /usr/bin/duf, /usr/bin/tmux
dpkg -S "$(which duf)" "$(which tmux)"     # both owned by dpkg
```

`~/.local/bin` precedes `/usr/bin` in PATH, so the old files had to be moved
out of the way, not just shadowed.

PATH note: `~/.pi/agent/bin` and `~/.local/bin` come before `/usr/bin`, so
`which rg` / `which fd` show pi's bundled copies even with apt installed.
Both have a tracking story (npm for pi's, dpkg for apt's); don't delete pi's
— the harness uses them.

Other CLI tools already dpkg-tracked: `fzf`, `jq`, `batcat` (package `bat`),
`eza`, `htop`, `ncdu`, `gh`, `pkexec`. Missing, with apt candidates if ever
needed: `bat` (use `batcat`), `btop`, `dust`, `tldr`, `trash-cli`.

## 3. Rule of thumb for new tools

```bash
apt-cache policy <pkg> | grep Candidate   # 1. apt first
# only if absent: uv tool / npm / official installer / pinned release binary
```

When a release binary is unavoidable, keep the download command and version
in the topic note and in home_config so the next machine (or reinstall) gets
the same version.

## Source

- https://wiki.debian.org/Apt
- https://docs.astral.sh/uv/ , https://docs.npmjs.com/
