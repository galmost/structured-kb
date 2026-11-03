# Brave Browser Install (Arch Linux)

Brave is in AUR as `brave-bin`.

## 1. Install from AUR

Use your preferred AUR helper:

```bash
yay -S brave-bin
# or
paru -S brave-bin
```

Or manually:

```bash
git clone https://aur.archlinux.org/brave-bin.git
cd brave-bin
makepkg -si
```

## 2. Verify

```bash
brave --version
```

## Troubleshooting

### Build fails

Missing dependencies — install `base-devel` and `git`.

### Signature error

Run `gpg --recv-keys <key-id>` from the PKGBUILD or use
`--skip-integrity-checks` as last resort.

### Brave not launching

```bash
update-desktop-database -q
```

### Sandbox issues

```bash
brave --no-sandbox
```

Not recommended. Fix kernel/user namespace support instead.

## Source

- [Brave AUR package](https://aur.archlinux.org/packages/brave-bin)
