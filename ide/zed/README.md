# Zed Editor Configuration

This folder contains the current Zed editor settings and configuration files.

## Current Setup

### File Explorer
- Aligned to the left (default in Zed).
- Toggle visibility: `Cmd/Ctrl + B`.

### Keybindings
- Quick file navigation: `Cmd/Ctrl + P`.
- Split editor: `Cmd/Ctrl + \`.
- Toggle terminal: `Cmd/Ctrl + ~`.

### Terminal Shell
- Integrated terminal runs zsh as a login shell, pinned in `settings.json`:

```json
"terminal": {
  "shell": {
    "with_arguments": {
      "program": "/usr/bin/zsh",
      "args": ["--login"]
    }
  }
}
```

Zed otherwise uses the shell from `/etc/passwd`; the explicit pin keeps the
terminal on zsh (with `~/.zshrc`, OMZ and the p10k prompt) even if the login
shell changes. Requires zsh installed, see `computer/debian/zsh/README.md`.

### Extensions
- List of installed extensions (if any):
  - None (default setup).

### Themes
- Current theme: Default (light/dark based on system settings).

## Configuration Files

The following files are copied from Zed's configuration directory:
- `settings.json`: User settings and preferences.
- `keymap.json`: Custom keybindings (if any).

## How to Apply These Settings

1. Copy the config files to Zed's configuration directory:
   - Linux: `~/.config/zed`
   - macOS: `~/Library/Application Support/zed`
2. Restart Zed to apply changes.

## Notes
- Zed is still in development, so some settings may change in future updates.
- Refer to [Zed's documentation](https://zed.dev/docs) for the latest configuration options.
