# Brave Browser Setup (Linux)

Brave is a privacy-focused Chromium-based browser with built-in ad blocking,
Tor support, and reward system.

## Install

Distro-specific install steps:

- Debian: see [computer/debian/brave/README.md](../../debian/brave/README.md)
- Arch: see [computer/arch/brave/README.md](../../arch/brave/README.md)

## Verify

```bash
brave-browser --version
# or on Arch
brave --version
```

## Common Troubleshooting

### Brave not launching

Check desktop environment integration:
```bash
update-desktop-database -q
```

### Sandbox issues

Brave uses Chromium sandbox. If crashes, try disabling:
```bash
brave-browser --no-sandbox
# or on Arch
brave --no-sandbox
```

Not recommended for security. Fix proper kernel/user namespace support instead.

## Source

- [Brave Linux installation guide](https://brave.com/linux/)
- [Brave AUR package](https://aur.archlinux.org/packages/brave-bin)
