# Daily git snapshot of the home folder (CachyOS rolling)

Home folder is a git repo of `git@ssh.bitbucket.org:galmost/gcachydeck_home.git` (`.git` in `~`). Systemd **user** timer commits and pushes allowlisted dotfiles once a day **directly to `main`** with a UTC timestamp commit message. History is a timeline, damage recoverable per file per day. Package lists dumped too, reinstall scriptable. Adapted from the Debian 13 note (`computer/debian/home-git-snapshot`).

## 1. Prerequisites

- Bitbucket SSH key set up and added in Bitbucket web UI (`~/.ssh/id_ed25519_bitbucket`), with `~/.ssh/config` covering **both** hostnames (Bitbucket moved SSH traffic to `ssh.bitbucket.org`):

```bash
ssh-keyscan -t ed25519,ecdsa,rsa bitbucket.org ssh.bitbucket.org >> ~/.ssh/known_hosts
```

```
Host bitbucket.org ssh.bitbucket.org
  HostName bitbucket.org
  User git
  IdentityFile ~/.ssh/id_ed25519_bitbucket
  IdentitiesOnly yes
```

- Repo `gcachydeck_home` created empty-ish on Bitbucket (initial commit with boilerplate `.gitignore` is fine).
- Git identity for commits: `git config user.name "..."` + `git config user.email "..."` (repo-local in `~` is enough).

## 2. Turn the home folder into the repo

Non-destructive: nothing existing is modified or deleted; HEAD is aligned with the remote first so the push is a fast-forward.

```bash
cd ~
git init -b main
git remote add origin git@ssh.bitbucket.org:galmost/gcachydeck_home.git
git fetch origin
git reset --soft origin/main   # align HEAD with remote, keep working tree untouched
```

## 3. Default-deny `.gitignore`

Write `~/.gitignore` (replaces the Bitbucket boilerplate on first commit). Only allowlisted dotfiles tracked; add a `!<path>` line per new dotfile, then verify:

```bash
git check-ignore -v <path>     # must NOT be ignored before git add
```

```
# Default-deny: only allowlisted dotfiles are tracked.
# Never allowlist secrets: ~/.ssh/id_*, ~/.pi/agent/auth.json, ~/.config/gh,
# ~/.gnupg, ~/.local/share/keyrings.
*
!.gitignore
!/.zshrc
!/.gitconfig
!/.gtkrc-2.0
!/.ssh/
!.ssh/config
!.ssh/known_hosts
!/.pi/
!/.pi/agent/
!/.pi/agent/settings.json
!/.pi/agent/models-store.json
!/.config/
!/.config/fish/
!/.config/fish/**
!/.config/alacritty/
!/.config/alacritty/**
!/.config/systemd/
!/.config/systemd/user/
!/.config/systemd/user/**
!galmost@GCachyDeck/
!galmost@GCachyDeck/**
```

Secrets NOT in git by design: `~/.ssh/id_*`, `~/.pi/agent/auth.json`, `~/.config/gh/` (hosts.yml holds the token), `~/.gnupg`, `~/.local/share/keyrings/`. Back up separately, encrypted, off-box.

## 4. Snapshot script + package lists + units

Script `~/galmost@GCachyDeck/bin/home-snapshot.sh` (chmod +x):

```bash
#!/usr/bin/env bash
# Daily git snapshot of the home folder: refresh package lists, commit
# allowlisted dotfiles, push straight to main of gcachydeck_home.
set -euo pipefail
cd "$HOME"

# In non-interactive contexts use the keyring ssh-agent socket so the
# Bitbucket key is available without a terminal prompt.
export SSH_AUTH_SOCK="${SSH_AUTH_SOCK:-/run/user/$(id -u)/keyring/ssh}"

# Refresh package lists (Arch equivalent of dpkg/apt selections dumps)
mkdir -p "$HOME/galmost@GCachyDeck/packages"
pacman -Qqe > "$HOME/galmost@GCachyDeck/packages/pacman-explicit.txt"
# -Qqm exits 1 when no foreign (AUR) packages installed — that is fine
pacman -Qqm > "$HOME/galmost@GCachyDeck/packages/pacman-foreign.txt" || true

git add -A
if ! git diff --cached --quiet; then
    git commit -m "$(date -u '+%Y-%m-%dT%H:%M:%SZ') chore(config): daily home snapshot"
    git push origin HEAD:main
fi
```

Units `~/.config/systemd/user/gcachydeck-home-snapshot.{service,timer}`:

```
# gcachydeck-home-snapshot.service
[Unit]
Description=Daily git snapshot of the home folder (gcachydeck_home)

[Service]
Type=oneshot
ExecStart=%h/galmost@GCachyDeck/bin/home-snapshot.sh
```

```
# gcachydeck-home-snapshot.timer
[Unit]
Description=Run gcachydeck-home-snapshot daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

## 5. First commit + enable

```bash
cd ~
git add -A
git commit -m "$(date -u '+%Y-%m-%dT%H:%M:%SZ') chore(config): initial home snapshot setup"
git push origin HEAD:main

systemctl --user daemon-reload
systemctl --user enable --now gcachydeck-home-snapshot.timer
systemctl --user list-timers gcachydeck-home-snapshot.timer
# OnCalendar=daily, Persistent=true — runs at 00:00, catches up after sleep
```

Manual run: `bash ~/galmost@GCachyDeck/bin/home-snapshot.sh`

## 6. Restore

```bash
cd ~ && git fetch origin
git log --oneline origin/main                   # pick a snapshot commit
git checkout origin/main -- <path>              # restore one file
git checkout origin/main -- .                   # restore everything tracked
# package lists for a fresh install:
#   pkexec pacman -S --needed $(cat galmost@GCachyDeck/packages/pacman-explicit.txt)
#   foreign/AUR packages from pacman-foreign.txt installed via yay/paru
```

## Troubleshooting

- **`pacman -Qqm` kills the script**: exits 1 when no AUR packages installed; with `set -e` the script aborts before `git add`. Fix: append `|| true`.
- **`Host key verification failed` / `ssh_askpass` error**: non-interactive shell cannot accept the host key prompt. Fix: `ssh-keyscan -t ed25519,ecdsa,rsa bitbucket.org ssh.bitbucket.org >> ~/.ssh/known_hosts`.
- **git clone via `ssh.bitbucket.org` fails but `bitbucket.org` works**: SSH config only matched one hostname. Use `Host bitbucket.org ssh.bitbucket.org` with `HostName bitbucket.org`.
- **`Author identity unknown` on commit**: set repo-local identity (`git config user.name/user.email` in `~`).
- **Push rejected (non-fast-forward)**: remote got commits meanwhile. Fix: `git pull --rebase origin main` then push; never force-push main.
- **Secret shows up in `git status`**: it is not allowlisted-safe — remove from index (`git rm --cached <path>`), add ignore/negation, verify with `git check-ignore -v <path>`.

## Source

- Adapted from `computer/debian/home-git-snapshot/README.md` (Debian 13, gark_home repo)
- https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
