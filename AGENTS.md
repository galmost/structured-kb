# structured-kb — conventions

## Repo layout

```
computer/<distro|domain>/<topic>/README.md
```

One topic per folder. One `README.md` per topic. Notes match distro in path (`computer/arch/...`, `computer/debian/...`). State releases covered.

## Note format

`README.md` shape:

1. `# <Topic> Setup (<distro> <version>)` — title name topic and target.
2. Short intro: what does, when need.
3. Numbered sections for steps: `## 1. Prerequisites`, then install, config, verify.
4. Exact commands in fenced `bash` blocks. Never paraphrase command.
5. `## Troubleshooting` at end: one subsection per known failure, shortest decisive fix.

## Style rules

- Commands verbatim. Copy-paste work as shown.
- Call out distro differences explicit ("Debian 13", "Ubuntu 24.04").
- Flag destructive or root steps in prose before command.
- In `computer/debian/...` notes, prefer `pkexec apt ...` over `sudo apt ...` when passwordless sudo unavailable (`sudo` prompt password in non-interactive shell; `pkexec` auth via polkit).
- Link source article at bottom under `## Source` when note adapted from somewhere.

## Commit convention

Conventional Commits. KB changes use `docs(kb)` scope:

```
docs(kb): add debian brave install notes
docs(kb): restructure linux folder to point to distro-specific steps
```

## Branch convention

Always create feature branch from `main`. Prefix: `feature/`, `fix/`, `docs/`, `refactor/`. Never push `main` direct. Always create or update remote PR for pushed branch (`gh pr create`, `gh pr edit` on updates) — pushed branch without PR incomplete.

## Worktree convention

Always work in separate git worktree, never main checkout. One worktree per branch, under `$VIBE_HOME/worktrees/` (default `~/.vibe/worktrees/`), per-repo bucket `<repo>-<sha256(common_git_dir)[:12]>/<name>/`.

- Create: `git worktree add -b <branch> <path> origin/main` — fetch first; new branch start from remote default, not current HEAD.
- Reuse worktree only when branch match and path valid (no symlinks, `.git` is file, same common git dir).
- Clean up via vibe worktree tooling, never `rm -rf`: dirty worktree snapshot to `refs/vibe/reaped/<name>` before removal; confirm before delete branch that pre-existed session.

## Agent behavior

- Like-named topic go in existing folder; only create new folder when no topic folder match.
- Never delete existing command or comment you not ask to change.
- Any `AGENTS.md` change must be followed by `/caveman-compress AGENTS.md` before commit.