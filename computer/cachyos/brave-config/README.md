# Brave debloat + dark mode (CachyOS)

Minimal Brave config. State lives in
`~/.config/BraveSoftware/Brave-Browser/Default/Preferences` (JSON) — not
tracked by home git (`.config/BraveSoftware` ignored). Set via
`brave://settings` GUI or by merging keys into Preferences with Brave closed.

## 1. Dark mode

```json
"browser": { "theme": { "color_scheme2": 2 } }
```

`color_scheme2`: 0=system, 1=light, **2=dark**. Already dark on this box.
GUI: `brave://settings/appearance` → Mode → Dark.

## 2. Debloat toggles (set false)

| feature | pref key |
|---|---|
| Rewards / BAT | `brave.rewards.enabled` |
| Wallet / Web3 | `brave.wallet.enabled` |
| Leo AI chat | `brave.ai_chat.enabled` |
| Brave Talk | `brave.brave_together.enabled` |
| News | `brave.news.enabled` |
| VPN | `brave.vpn.enabled` |
| Sidebar | `brave.sidebar.enabled` |
| Background apps | `background_mode.enabled` |
| Search suggestions | `search.suggest_enabled` |
| NTP widgets/background | `brave.new_tab_page.show_*` |

Keep **Shields ON** — privacy, not bloat.

## 3. Verify

```bash
python3 -c "
import json
p=json.load(open('$HOME/.config/BraveSoftware/Brave-Browser/Default/Preferences'))
print('dark:', p['browser']['theme'].get('color_scheme2'))
print('rewards:', p.get('brave',{}).get('rewards',{}).get('enabled'))
"
```

## Troubleshooting

- Edits to Preferences ignored — Brave rewrites the file on exit; edit with Brave **closed**, or use the GUI.
- `color_scheme2` back to 0 — KDE/system theme changed; re-set to 2.

## Source

- brave://settings/appearance
- Chromium `browser.theme.color_scheme2` enum (0 system / 1 light / 2 dark)
