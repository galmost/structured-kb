# Dell XPS Fingerprint Reader Setup (Goodix 27c6:532d)

This guide outlines the steps to install and configure the Goodix fingerprint reader on Arch Linux for Dell laptops (specifically XPS models with device ID `27c6:532d`).

## 1. Hardware Identification
Verify your device ID:
```bash
lsusb | grep -i finger
```
Expected output: `Bus XXX Device XXX: ID 27c6:532d Shenzhen Goodix Technology Co.,Ltd. Fingerprint`

## 2. Resolve Package Conflicts (Pre-requisite)
If you encounter errors related to `libgcc` or `libstdc++` existing in the filesystem (owned by `gcc-libs`), run:
```bash
sudo pacman -S --overwrite '/usr/lib/libgcc_s.so*,/usr/lib/libstdc++.so*,/usr/share/locale/*/LC_MESSAGES/libstdc++.mo,/usr/share/licenses/gcc-libs/*' libgcc libstdc++ gcc-libs
```

## 3. Install Driver and Daemon
Install the required AUR packages (using `yay` or your preferred AUR helper):
```bash
yay -S libfprint-2-tod1-goodix fprintd
```
*Note: This will also pull in `libfprint-tod` as a dependency.*

## 4. Enable and Start Service
```bash
sudo systemctl enable --now fprintd
```

## 5. Enroll Fingerprint
Enroll your right index finger (or follow prompts for others):
```bash
fprintd-enroll
```
*Keep swiping your finger until it says "Enrollment completed".*

## 6. Configure PAM Authentication
To use the fingerprint for `sudo`, edit `/etc/pam.d/sudo`:
Add this line to the **top** of the file:
```text
auth      sufficient    pam_fprintd.so
```

To use it for login (GDM/SDDM) or lock screens, you may also need to modify `/etc/pam.d/system-local-login` or similar, but start with `sudo` to verify it works.

## Troubleshooting
- If `fprintd-enroll` says "ListDevices failed", ensure the `fprintd` service is running and your user has permissions (usually handled by `polkit` or being in the `input` group).
- Check logs: `journalctl -u fprintd`
