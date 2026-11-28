# Wake-on-LAN Setup (Debian 13)

WoL keeps the NIC powered while the machine sleeps or is off, so a 96-byte magic packet (`0xFF`×6 + MAC×16) powers it on from a host on the same LAN. No button press needed.

| Wake from | Kernel state | Needs BIOS/UEFI changes |
| --- | --- | --- |
| Suspend (S3) / `freeze` | RAM powered, driver armed | No |
| Full poweroff (S5) | Board keeps 5V on the PCIe slot | Yes |

Tested on Debian 13 (trixie), kernel 6.12.115+deb13.1-amd64, NetworkManager 1.52.1, ethtool 6.14.2, ASRock A620I Lightning WiFi (Realtek RTL8125, in-tree `r8169`). Wired interface only — wireless NICs do not listen for magic packets when off.

## 0. Identify interface, driver, MAC

Read-only, run as normal user:

```bash
ip -br link
readlink /sys/class/net/enp11s0/device/driver
cat /sys/class/net/enp11s0/device/uevent
nmcli -t -f NAME,TYPE,DEVICE,STATE connection show --active
```

On the test host:

```
enp11s0          UP             9c:6b:00:34:59:d2 <BROADCAST,MULTICAST,UP,LOWER_UP>
r8169
DRIVER=r8169
PCI_ID=10EC:8125
Wired connection 1:802-3-ethernet:enp11s0:activated
```

Substitute interface (`enp11s0`), connection name (`Wired connection 1`) and MAC below.

## 1. Arm WoL (root step, link must be up)

```bash
pkexec apt install -y ethtool
pkexec ethtool -s enp11s0 wol g
pkexec ethtool enp11s0 | grep -i wake-on    # Wake-on: g
```

`g` = magic packet. Reading the setting also needs root. Does not survive reboot — sections 2-4 do.

## 2. Persist in NetworkManager

NetworkManager 1.44+ re-applies WoL on every connection activation (trixie ships 1.52.1):

```bash
pkexec nmcli connection modify "Wired connection 1" 802-3-ethernet.wake-on-lan magic
nmcli -f 802-3-ethernet.wake-on-lan connection show "Wired connection 1"   # magic
```

Use `magic`, not `phy` — `phy` wakes on any link-state change (switch renegotiation, cable replug).

## 3. Re-arm at boot and during shutdown (needed for S5)

NetworkManager arms the card on activation, but shutdown tears the network down and the driver clears the WoL bit. A oneshot unit with `RemainAfterExit=yes` runs `ExecStart` at boot and `ExecStop` late in shutdown.

Root step:

```bash
sudo tee /etc/systemd/system/wol-rearm.service > /dev/null <<'EOF'
[Unit]
Description=Keep Wake-on-LAN armed on enp11s0
Documentation=man:ethtool(8)
Wants=sys-subsystem-net-devices-enp11s0.device
After=sys-subsystem-net-devices-enp11s0.device
After=NetworkManager.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/sbin/ethtool -s enp11s0 wol g
ExecStop=/usr/sbin/ethtool -s enp11s0 wol g

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable wol-rearm.service
systemctl is-enabled wol-rearm.service   # enabled
systemctl is-active wol-rearm.service    # active
```

Do not add `DefaultDependencies=no` — without normal dependencies systemd will not stop the unit on poweroff and `ExecStop` never runs.

## 4. Re-arm after resume

NetworkManager re-applies the setting on resume; this hook covers the gap. Root step:

```bash
sudo tee /lib/systemd/system-sleep/wol-rearm.sh > /dev/null <<'EOF'
#!/bin/sh
# systemd-sleep hook: $1 = pre|post, $2 = suspend|hibernate
if [ "$1" = "post" ]; then
    /usr/sbin/ethtool -s enp11s0 wol g
fi
EOF

sudo chmod 0755 /lib/systemd/system-sleep/wol-rearm.sh
```

## 5. UEFI/BIOS settings for wake from poweroff

S5 wake needs standby power on the PCIe slot. ASRock AMI UEFI (`F2` at POST → Advanced Mode), tested on A620I Lightning WiFi BIOS 3.01:

| Setting | Path | Value |
| --- | --- | --- |
| PCIE Devices Power On | Advanced → ACPI Configuration | Enabled |
| Deep Sleep | Advanced → ACPI Configuration | Disabled |

Deep Sleep (also ErP / ErP Ready / EuPlus) cuts 5V standby to save under a watt and kills S5 wake — it often hides the PCIe power-on option. Other vendors: ASUS `Power On By PCI-E`, Gigabyte `Power On By PCI-E/PCI`, MSI `Wake on LAN` + `ErP Ready = Disabled`.

## 6. Wake from another host

```bash
sudo apt install -y wakeonlan        # UDP magic packet, no root to send
wakeonlan 9c:6b:00:34:59:d2
wakeonlan -i 192.168.1.255 9c:6b:00:34:59:d2   # explicit subnet broadcast
```

`etherwake` builds a raw Ethernet frame and needs root plus the sender interface: `sudo etherwake -i <sender-interface> 9c:6b:00:34:59:d2`.

No sender installed — netcat:

```bash
MAC=9c:6b:00:34:59:d2
xxd -r -p <<< "ffffffffffff$(echo ${MAC//:/} | sed 's/\(..\)/\1\1\1\1\1\1\1\1\1\1\1\1\1\1\1\1/g')" \
  | nc -w1 -u -b 192.168.1.255 9
```

Test in this order — the two cases fail for different reasons:

```bash
sudo systemctl suspend      # S3: only sections 1-4 needed
sudo systemctl poweroff     # S5: needs section 5 as well
```

## Troubleshooting

### `Wake-on: d` after setting `g`

Something reset it:

```bash
pkexec ethtool enp11s0 | grep -i wake-on
journalctl -b -u wol-rearm.service
```

### `Cannot set new wake-on-lan settings: Operation not supported`

Interface down, or the driver does not expose WoL. Bring the link up and retry; confirm `readlink /sys/class/net/enp11s0/device/driver` shows `r8169` (out-of-tree `r8125` not always supported; use in-tree `r8169`).

### Wakes from suspend but not from poweroff

Firmware, not Linux. Confirm `pkexec ethtool enp11s0 | grep -i wake-on` shows `g` before poweroff, then disable Deep Sleep / ErP and enable PCIE Devices Power On (§5). If link LEDs go dark after poweroff there is no standby power — S5 wake is impossible.

### Machine powers on by itself

Confirm WoL is `magic` not `phy`, then check other wake sources:

```bash
journalctl -b | grep -iE "wake-up|wake.*device|ACPI.*wake"
cat /sys/bus/usb/devices/*/power/wakeup 2>/dev/null | sort | uniq -c
echo disabled | sudo tee /sys/bus/usb/devices/<device>/power/wakeup
```

### Magic packet sent, nothing happens

- Sender and target on different subnets — broadcast does not cross routers unless directed broadcasts are forwarded.
- Switch dropped the frame (target MAC not learned while off) — send to the subnet broadcast, not a stale unicast ARP entry: `wakeonlan -i 192.168.1.255 <mac>`.
- Sent from Wi-Fi — send from a wired host on the same segment.
- Firewall on sender or intermediate host; a target-side firewall is irrelevant (OS is off).

### Wake works once, then stops

WoL bit cleared by resume or driver reload — keep both `wol-rearm.service` and the system-sleep hook installed.

## Source

- Linux `r8169` driver: https://github.com/torvalds/linux/tree/master/drivers/net/ethernet/realtek
- NetworkManager `802-3-ethernet.wake-on-lan`: https://networkmanager.dev/docs/api/latest/settings-5.html
- `ethtool(8)` — `show-wol` / `wol`
- ASRock UEFI WoL option names: https://n-archives.net/software/nwol/wol-pc-setting/bios-setting-asrock.html
