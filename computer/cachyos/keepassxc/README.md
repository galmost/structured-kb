# KeePassXC + Brave browser integration (CachyOS)

KeePassXC 2.8.0 (`pkexec pacman -S keepassxc`) with KeePassXC-Browser
extension in Brave so login fields autofill from the vault.

## 1. Install

```bash
pkexec pacman -S --needed keepassxc
keepassxc --version    # 2.8.0
```

## 2. Enable browser integration (non-interactive)

`~/.config/keepassxc/keepassxc.ini`:

```ini
[Browser]
Enabled=true
```

(GUI equivalent: Settings → Browser Integration → enable.)

## 3. Add extension to Brave

Store install (GUI, one click) — KeePassXC-Browser:
https://chromewebstore.google.com/detail/keepassxc-browser/oboonakemofpalcgghocfoadofidjkkk

Brave is Chromium — Chrome Web Store works directly.

## 4. Connect

1. KeePassXC → Settings → Browser Integration → **Connect** → give the browser a name (e.g. `brave`) → Save.
2. Extension popup (toolbar icon) → **Connect** → approve the named browser.
3. Test: open a site with a saved login, click the 🔑 icon in the field, or unlock vault and check a field autofills.

## Troubleshooting

- Extension icon shows "not connected" — vault must be **unlocked** first; KeePassXC ↔ extension handshake happens on unlock.
- Multiple browsers — each needs its own Connect name in KeePassXC.
- `Enabled=true` but no handshake — restart KeePassXC after editing ini.

## Source

- https://keepassxc.org/docs/KeePassXC_GettingStarted.html#_browser_integration
- Extension: Chrome Web Store `oboonakemofpalcgghocfoadofidjkkk`
