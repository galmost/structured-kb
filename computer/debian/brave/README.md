# Brave Browser Install (Debian)

## 1. Prerequisites

```bash
pkexec apt install -y curl gnupg
```

## 2. Add Brave repository

```bash
curl -fsSL https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg | pkexec gpg --dearmor -o /usr/share/keyrings/brave-browser-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | pkexec tee /etc/apt/sources.list.d/brave-browser-release.list
```

## 3. Install

```bash
pkexec apt update
pkexec apt install -y brave-browser
```

## 4. Verify

```bash
brave-browser --version
```

## 5. Tested

Debian trixie, actual commands run. Result: Brave Browser 156.1.98.63.

## Troubleshooting

### Repository errors

`404 Not Found` — check URL. Brave changed from `brave.com` to
`brave-browser-apt-release.s3.brave.com` hosting.

### Brave not launching

```bash
update-desktop-database -q
```

### Sandbox issues

```bash
brave-browser --no-sandbox
```

Not recommended. Fix kernel/user namespace support instead.

## Source

- [Brave Linux installation guide](https://brave.com/linux/)
