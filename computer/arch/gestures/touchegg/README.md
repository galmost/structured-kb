# Touchégg Setup (Arch Linux)

Touchpad/touchscreen gesture daemon, X11 and Wayland, XML gesture-to-action mappings.

## 1. Install

```bash
pacman -S touchegg
flatpak install com.github.joseexposito.touche   # optional GUI tweaker
```

## 2. Enable the daemon

```bash
sudo systemctl enable --now touchegg
systemctl status touchegg
```

Run as system service; it handles input-device access. No `~/.config/autostart` entry needed.

## 3. Configuration

| Scope | Path |
|---|---|
| System-wide | `/etc/xdg/touchegg/touchegg.conf` |
| Per-user | `~/.config/touchegg/touchegg.conf` |

Per-user config wins when present:

```bash
mkdir -p ~/.config/touchegg
cp /etc/xdg/touchegg/touchegg.conf ~/.config/touchegg/touchegg.conf
```

Example — three-finger swipe right sends Ctrl+Alt+Left (browser back):

```xml
<gesture type="SWIPE" fingers="3" direction="RIGHT">
  <action type="SEND_KEYS">
    <keys>CTRL_L+Alt_L+Left</keys>
    <repeat>false</repeat>
  </action>
</gesture>
```

## Source

- [Touchégg installation guide](https://github.com/JoseExposito/touchegg/tree/master/installation#readme)
- [Touché GUI tweaker (Flathub)](https://flathub.org/apps/com.github.joseexposito.touche)
