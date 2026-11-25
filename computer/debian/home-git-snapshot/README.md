# Daily git snapshot of the home folder (Debian 13)

Home folder is git worktree of `git@ssh.bitbucket.org:galmost/gark_home.git` (`.git` in `~`). Systemd **user** timer commits pushes tracked dotfiles once a day **directly to `main`** with UTC timestamp commit message. History is timeline, damage recoverable per file per day. Package lists dumped too, reinstall scriptable. Repo convention (see `~/AGENTS.md`): no feature branches or PRs, commit push straight to `main`.

## 1. What is stored

- All allowlisted dotfiles (`.gitignore` is default-deny): `~/.zshrc`, `~/.ssh/config`, `~/.pi/agent/` minus secrets (`auth.json` stays ignored), `~/.config/...`, `galmost@GArk/**`.
- `galmost@GArk/packages/dpkg-selections.txt` — `dpkg --get-selections` (minus deinstall).
- `galmost@GArk/packages/apt-manual.txt` — `apt-mark showmanual`.
- Script: `galmost@GArk/bin/home-snapshot.sh`.
- Units: `~/.config/systemd/user/gark-home-snapshot.{service,timer}`.

Secrets NOT in git by design: `~/.pi/agent/auth.json`, `~/.ssh/id_*`, `~/.local/share/keyrings/`, `~/.gnupg`, `~/.config/gh`. Back up separately, encrypted (age/gpg) to off-box target — see backup note (computer/debian/backup, when written).

## 2. How it runs

```bash
systemctl --user enable --now gark-home-snapshot.timer
systemctl --user list-timers gark-home-snapshot.timer
# OnCalendar=daily, Persistent=true — runs at 00:00, catches up after sleep
```

Script `cd ~`, regenerates package lists, `git add -A`, commits only if changed with message `<UTC timestamp> chore(config): daily home snapshot`, pushes `HEAD:main`. In non-interactive contexts exports `SSH_AUTH_SOCK=/run/user/$(id -u)/keyring/ssh` so Bitbucket key from GNOME keyring agent is used (see ssh-bitbucket-keyring note).

Manual run: `bash ~/galmost@GArk/bin/home-snapshot.sh`

## 3. Restore

```bash
cd ~ && git fetch origin
git log --oneline origin/main                   # pick a snapshot commit
git checkout origin/main -- <path>              # restore one file
git checkout origin/main -- .                   # restore everything tracked
# package lists for a fresh install:
#   pkexec dpkg --set-selections < galmost@GArk/packages/dpkg-selections.txt
#   pkexec apt-get dselect-upgrade   (or: xargs apt-get install < apt-manual.txt)
```

## 4. Caveats

- Only allowlisted paths tracked — new dotfiles need `!<path>` line in `~/.gitignore` first, then `git add`.
- `git add -A` respects ignore rules; check with `git check-ignore -v <path>` before adding anything new, never secrets.
- Timer is user unit: runs only while user session active; `Persistent=true` makes it fire immediately after login if run missed.

## Source

- home_config conventions: `~/AGENTS.md` in gark_home repo (push directly to main, timestamped commit prefix `YYYY-MM-DDTHH:MM:SSZ `)
- ssh-bitbucket-keyring note (keyring agent socket)
- https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html