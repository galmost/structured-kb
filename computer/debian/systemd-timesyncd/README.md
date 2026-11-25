# systemd-timesyncd (NTP) on Debian 13

Enables network time sync so the clock doesn't drift. Timezone was already
`Europe/Bucharest`; the missing piece was NTP (`System clock synchronized: no`).

## 1. Install and enable

```bash
pkexec apt-get install -y systemd-timesyncd
pkexec systemctl enable --now systemd-timesyncd
```

In non-interactive shells use `pkexec`, not `sudo` (sudo prompts for a
password; pkexec authenticates via polkit). If pkexec answers
`Request dismissed`, there is no polkit agent in that session — run the
commands from a real login shell instead.

## 2. Verify

```bash
timedatectl
#   Local time: ... EET
#   Time zone: Europe/Bucharest (EET, +0200)
#   System clock synchronized: yes
systemctl is-active systemd-timesyncd   # active
timedatectl timesync-status              # NTP peers and last sync
```

## 3. Quirks

- `pkexec timedatectl set-ntp true` fails with `Failed to set ntp: NTP not
  supported` even after timesyncd is running — timedated doesn't see it until
  restarted. The sync itself works; `System clock synchronized: yes` is the
  check that matters.
- `NTP service` may still print `n/a` in `timedatectl`; ignore it when
  `synchronized: yes`.
- On first sync the clock can jump (observed ~2h drift corrected on this
  host). Anything timestamp-sensitive (TLS, git commits, logs) should be
  re-checked right after enabling.
- Set the zone explicitly if needed: `pkexec timedatectl set-timezone Europe/Bucharest`.

## 4. Related

- Boot-time services enabled on this host are tracked here per topic folder;
  this note covers only time sync.

## Source

- `man systemd-timesyncd.service`, `man timedatectl`
- https://wiki.debian.org/SystemdTimesyncd
