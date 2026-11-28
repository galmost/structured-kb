# structured-kb — conventions

## Layout

```
computer/<distro|domain>/<topic>/README.md
```

One topic per folder, one `README.md` per topic. Distro in path (`computer/arch/...`, `computer/debian/...`). State releases covered.

## Note format

1. `# <Topic> Setup (<distro> <version>)`.
2. One-paragraph intro: what it does, when you need it.
3. Numbered sections: `## 1. Prerequisites`, then install, config, verify.
4. Exact commands in fenced `bash` blocks — never paraphrase.
5. `## Troubleshooting` last: one subsection per known failure, shortest decisive fix.

Say each thing once. Link to the note that owns a topic instead of restating it.

## Style

- Commands verbatim; copy-paste works as shown.
- Name distro versions explicitly ("Debian 13", "Ubuntu 24.04").
- Flag destructive or root steps in prose before the command.
- `computer/debian/...`: prefer `pkexec apt ...` over `sudo apt ...` — `sudo` prompts for a password in non-interactive shells, `pkexec` authenticates via polkit.
- Adapted from an article? Link it under `## Source`.

## Commits

Conventional Commits, scope `docs(kb)`:

```
docs(kb): add debian brave install notes
docs(kb): restructure linux folder to point to distro-specific steps
```

## Branches

Branch from `main`. Prefix `feature/`, `fix/`, `docs/`, `refactor/`. Never push `main` directly. Every pushed branch gets a PR — `gh pr create`, `gh pr edit` on updates.

## Worktrees

Always work in a separate worktree, never the main checkout. One worktree per branch under `$VIBE_HOME/worktrees/` (default `~/.vibe/worktrees/`), bucketed per repo as `<repo>-<sha256(common_git_dir)[:12]>/<name>/`.

- Create: fetch first, then `git worktree add -b <branch> <path> origin/main` — new branches start from the remote default, not current HEAD.
- Reuse a worktree only when the branch matches and the path is valid: no symlinks, `.git` is a file, same common git dir.
- Clean up with the vibe worktree tooling, never `rm -rf`: snapshot a dirty worktree to `refs/vibe/reaped/<name>` before removal; confirm before deleting a branch that pre-existed the session.

## Agents

- Like-named topics go in the existing folder; create a folder only when no topic matches.
- Never delete a command or comment you were not asked to change.
- Any `AGENTS.md` change must be followed by `/caveman-compress AGENTS.md` before commit.
