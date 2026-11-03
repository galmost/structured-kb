# structured-kb — conventions

## Repo layout

```
computer/<distro|domain>/<topic>/README.md
```

One topic per folder, one `README.md` per topic. Notes apply to the distro
named on their path (`computer/arch/...`, `computer/debian/...`); say
explicitly which releases a note covers.

## Note format

Every `README.md` follows this shape:

1. `# <Topic> Setup (<distro> <version>)` — title names the topic and target.
2. Short intro: what this does and when you need it.
3. Numbered sections for steps: `## 1. Prerequisites`, then install,
   configuration, verification.
4. Exact commands in fenced `bash` blocks. Never paraphrase a command.
5. `## Troubleshooting` at the end: one subsection per known failure,
   with the shortest decisive fix.

## Style rules

- Commands verbatim. Copy-paste must work as shown.
- Call out distro differences explicitly ("Debian 13", "Ubuntu 24.04").
- Flag destructive or root steps in prose before the command.
- In `computer/debian/...` notes, prefer `pkexec apt ...` over `sudo apt ...`
  when passwordless sudo is unavailable (`sudo` prompts for a password in a
  non-interactive shell; `pkexec` authenticates via polkit).
- Link the source article at the bottom under `## Source` when the note
  is adapted from somewhere.

## Commit convention

Use Conventional Commits. For knowledge base changes, use `docs(kb)` scope:

```
docs(kb): add debian brave install notes
docs(kb): restructure linux folder to point to distro-specific steps
```

## Branch convention

Always create feature branches from `main`. Name branches with prefix:
`feature/`, `fix/`, `docs/`, `refactor/`. Never push to `main` directly.

## Agent behavior

- Like-named topics go in the existing folder; only create a new folder
  when no topic folder matches.
- Never delete an existing command or comment you were not asked to change.
