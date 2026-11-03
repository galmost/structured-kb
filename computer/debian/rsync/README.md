# rsync Setup (Debian / Ubuntu)

Installs `rsync` from the distro archive. Required by Zed's remote development
(Zed shells out to `rsync` when connecting to a remote SSH server).

## 1. Install

```bash
pkexec apt install -y rsync
```

Use `sudo apt install -y rsync` instead if passwordless sudo is configured.

Verify:

```bash
rsync --version
```

Debian 13 ships rsync 3.5.0 (protocol version 32).

## 2. Zed remote development

Zed uses rsync to sync project files when you open a folder over SSH
(`Remote Projects` / `ssh://user@host/path`). No extra config needed —
Zed finds rsync on `PATH`. If the remote host lacks rsync, install it there
too:

```bash
ssh user@host 'pkexec apt install -y rsync'
```

## Common usage

```bash
# Mirror a local dir to a remote host
rsync -avz --delete ./ user@host:/path/dest/

# Dry run first
rsync -avzn --delete ./ user@host:/path/dest/

# Exclude patterns
rsync -avz --exclude 'node_modules' --exclude '.git' ./ user@host:/path/dest/
```

Flags: `-a` archive (recursive, preserves perms/times/symlinks), `-v` verbose,
`-z` compress during transfer, `-n` dry run, `--delete` remove extraneous files
on destination.

## Source

- [rsync man page](https://linux.die.net/man/1/rsync)
- [Zed remote development](https://zed.dev/docs/remote-development)
