# Daily git snapshot of the home folder (Debian 13)

The home folder is itself the git worktree of `git@ssh.bitbucket.org:galmost/gark_home.git`
(`.git` lives in `~`). A systemd **user** timer commits and pushes all tracked
dotfiles once a day **directly to `main`** with a UTC-timestamped commit
message, so the history doubles as a timeline and agent damage is recoverable
per file and per day. Package lists are dumped alongside, so a reinstall is
scriptable. Repo convention (see `~/AGENTS.md`): no feature branches or PRs,
commit and push straight to `main`.

## 1. What is stored

- All allowlisted dotfiles (`.gitignore` is default-deny): `~/.zshrc`,
  `~/.ssh/config`, `~/.pi/agent/` minus secrets (`auth.json` stays ignored),
  `~/.config/...`, `galmost@GArk/**`.
- `galmost@GArk/packages/dpkg-selections.txt` — `dpkg --get-selections` (minus deinstall).
- `galmost@GArk/packages/apt-manual.txt` — `apt-mark showmanual`.
- Script: `galmost@GArk/bin/home-snapshot.sh`.
- Units: `~/.config/systemd/user/gark-home-snapshot.{service,timer}`.

Secrets are NOT in git by design: `~/.pi/agent/auth.json`, `~/.ssh/id_*`,
`~/.local/share/keyrings/`, `~/.gnupg`, `~/.config/gh`. Back those up
separately, encrypted (age/gpg) to an off-box target — see the backup note
(computer/debian/backup, when written).

## 2. How it runs

```bash
systemctl --user enable --now gark-home-snapshot.timer
systemctl --user list-timers gark-home-snapshot.timer
# OnCalendar=daily, Persistent=true — runs at 00:00, catches up after sleep
```

The script `cd ~`, regenerates the package lists, `git add -A`, commits only
if something changed with message
`<UTC timestamp> chore(config): daily home snapshot`, and pushes
`HEAD:main`. In non-interactive contexts it exports
`SSH_AUTH_SOCK=/run/user/$(id -u)/keyring/ssh` so the Bitbucket key from the
GNOME keyring agent is used (see ssh-bitbucket-keyring note).

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

- Only allowlisted paths are tracked — new dotfiles need a `!<path>` line in
  `~/.gitignore` first, then `git add`.
- `git add -A` respects the ignore rules; check with
  `git check-ignore -v <path>` before adding anything new, never secrets.
- The timer is a user unit: it runs only while the user session is active;
  `Persistent=true` makes it fire immediately after login if a run was
  missed.

## Source

- home_config conventions: `~/AGENTS.md` in the gark_home repo (push directly
  to main, timestamped commit prefix `YYYY-MM-DDTHH:MM:SSZ `)
- ssh-bitbucket-keyring note (keyring agent socket)
- https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
