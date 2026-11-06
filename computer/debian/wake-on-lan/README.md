# Wake-on-LAN Setup (Debian 13)

Wake-on-LAN (WoL) keeps the network card powered while the machine is asleep or
off, and wakes the machine when it receives a magic packet: a 96-byte frame
containing six `0xFF` bytes followed by the target MAC address repeated sixteen
times. Use it to power on a headless or tucked-away box from another host on the
same LAN, without touching a physical power button.

Two distinct cases, and they need different work:

| Wake from | Kernel state | Needs BIOS/UEFI changes |
| --- | --- | --- |
| Suspend to RAM (S3) / `freeze` | RAM powered, NIC driver already armed | No |
| Full poweroff (S5) | Board must keep 5V standby on the PCIe slot | Yes |

This note covers both. It was tested on Debian 13 (trixie), kernel
6.12.115+deb13.1-amd64, NetworkManager 1.52.1, `ethtool` 6.14.2, on an ASRock
A620I Lightning WiFi board with a Realtek RTL8125 2.5GbE controller driven by
the in-tree `r8169` driver.

## 0. Identify the interface, driver and MAC

Run these as a normal user. Nothing here changes state.

```bash
ip -br link
readlink /sys/class/net/enp11s0/device/driver
cat /sys/class/net/enp11s0/device/uevent
nmcli -t -f NAME,TYPE,DEVICE,STATE connection show --active
```

On the test host this gives:

```
enp11s0          UP             9c:6b:00:34:59:d2 <BROADCAST,MULTICAST,UP,LOWER_UP>
r8169
DRIVER=r8169
PCI_ID=10EC:8125
Wired connection 1:802-3-ethernet:enp11s0:activated
```

Note the interface name (`enp11s0`), the connection name
(`Wired connection 1`), and the MAC. Substitute all three below. WoL works on
the wired interface only — a wireless NIC does not listen for magic packets
while the host is off.

## 1. Install ethtool

Root step: this installs a package. `sudo` prompts for a password in a
non-interactive shell; `pkexec` authenticates through polkit instead.

```bash
pkexec apt install -y ethtool
```

Use `sudo apt install -y ethtool` if passwordless sudo is configured.

## 2. Arm WoL on the running interface

Root step. Run this while the link is up — some drivers reject the call on a
down interface.

```bash
pkexec ethtool -s enp11s0 wol g
pkexec ethtool enp11s0 | grep -i wake-on
```

Expected output:

```
Wake-on: g
```

`g` means "magic packet". Reading the setting also requires root, so keep the
`pkexec` prefix on the verification command.

This does not survive a reboot on its own. Sections 3 to 5 make it persistent.

## 3. Persist it in NetworkManager

NetworkManager 1.44 and later have a native per-connection WoL setting, which
is re-applied every time the connection activates. Debian 13 ships 1.52.1.
Root/polkit step:

```bash
pkexec nmcli connection modify "Wired connection 1" 802-3-ethernet.wake-on-lan magic
nmcli -f 802-3-ethernet.wake-on-lan connection show "Wired connection 1"
```

Expected output:

```
802-3-ethernet.wake-on-lan:             magic
```

Reading the setting works as a normal user; only the `modify` needs polkit.

Use `magic`, not `phy`. `phy` wakes on any link-state change, which powers the
machine on whenever a switch port renegotiates or a cable is unplugged.

## 4. Re-arm at boot and during shutdown

Needed for wake from poweroff. NetworkManager arms the card when the connection
activates, but the shutdown path tears the network down afterwards, and the
driver can clear the WoL bit on its way out. A `Type=oneshot` service with
`RemainAfterExit=yes` runs `ExecStart` at boot and `ExecStop` late during
shutdown, so the card is re-armed on both edges.

Root step. This writes a unit file into `/etc/systemd/system/`.

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
```

Do not add `DefaultDependencies=no` to this unit. Without the normal
dependencies systemd does not stop the service on poweroff, so `ExecStop` never
runs and the card is left unarmed.

Verify:

```bash
systemctl is-enabled wol-rearm.service
systemctl is-active wol-rearm.service
```

Both must print `enabled` and `active`.

## 5. Re-arm after resume

After a resume, NetworkManager re-activates the connection and re-applies the
setting, but a `system-sleep` hook costs nothing and covers the case where it
does not. Root step:

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

## 6. UEFI/BIOS settings for wake from poweroff

Suspend works without touching firmware. Poweroff does not: the board must keep
standby power on the PCIe slot. On ASRock boards with an AMI UEFI
(tested on A620I Lightning WiFi, BIOS 3.01), press `F2` at POST, enter Advanced
Mode, then:

| Setting | Path | Value |
| --- | --- | --- |
| PCIE Devices Power On | Advanced → ACPI Configuration | Enabled |
| Deep Sleep | Advanced → ACPI Configuration | Disabled |

Deep Sleep (also labelled ErP, ErP Ready or EuPlus on other boards) must be
disabled. It cuts 5V standby to save less than a watt, which kills S5 wake and
often hides the PCIe power-on option from the menu entirely.

The same options on other vendors: ASUS `Power On By PCI-E`, Gigabyte
`Power On By PCI-E/PCI`, MSI `Wake on LAN` / `ErP Ready = Disabled`.

## 7. Wake the machine from another host

Install a sender on any host on the same LAN. `wakeonlan` sends a UDP magic
packet and needs no root:

```bash
sudo apt install -y wakeonlan        # Debian/Ubuntu
wakeonlan 9c:6b:00:34:59:d2
```

Target the subnet broadcast explicitly if the default does not arrive:

```bash
wakeonlan -i 192.168.1.255 9c:6b:00:34:59:d2
```

`etherwake` builds the raw Ethernet frame instead of a UDP packet, so it needs
root and the interface to be given with `-i`:

```bash
sudo apt install -y etherwake
sudo etherwake -i <sender-interface> 9c:6b:00:34:59:d2
```

With no sender installed, netcat works:

```bash
# FF*6 then MAC*16, sent to UDP port 9 on the subnet broadcast
MAC=9c:6b:00:34:59:d2
xxd -r -p <<< "ffffffffffff$(echo ${MAC//:/} | sed 's/\(..\)/\1\1\1\1\1\1\1\1\1\1\1\1\1\1\1\1/g')" \
  | nc -w1 -u -b 192.168.1.255 9
```

Test in this order, because the two cases fail for different reasons:

```bash
sudo systemctl suspend      # S3: should work with only sections 1-5
sudo systemctl poweroff     # S5: needs section 6 as well
```

## Troubleshooting

### `Wake-on: d` after setting `g`

The driver reset it. Check whether something else owns the setting:

```bash
pkexec ethtool enp11s0 | grep -i wake-on
journalctl -b -u wol-rearm.service
```

### `Cannot set new wake-on-lan settings: Operation not supported`

The interface is down, or the driver does not expose WoL. Bring the link up and
retry, and confirm the driver:

```bash
readlink /sys/class/net/enp11s0/device/driver
```

`r8169` supports `g`. Out-of-tree vendor drivers (`r8125` from Realtek) do not
always; use the in-tree `r8169` on Debian 13.

### Wakes from suspend but not from poweroff

Firmware, not Linux. Confirm the OS side is armed, then fix the BIOS:

```bash
pkexec ethtool enp11s0 | grep -i wake-on   # must show g before poweroff
```

Disable Deep Sleep / ErP and enable PCIE Devices Power On (section 6). Check
that the link LEDs stay lit after poweroff — no LEDs means no standby power, so
no S5 wake is possible.

### Machine powers on by itself

Something other than a magic packet is waking it. Confirm WoL is `magic` and
not `phy`, then look at the other wake sources:

```bash
journalctl -b | grep -iE "wake-up|wake.*device|ACPI.*wake"
cat /sys/bus/usb/devices/*/power/wakeup 2>/dev/null | sort | uniq -c
```

Disable a noisy USB device with:

```bash
echo disabled | sudo tee /sys/bus/usb/devices/<device>/power/wakeup
```

### Magic packet sent, nothing happens

The packet is not reaching the NIC. Most causes:

- Sender and target on different subnets. A broadcast from another subnet does
  not cross a router unless the router forwards directed broadcasts.
- The switch dropped the frame because it has not learned the target MAC while
  the target is off. Send to the subnet broadcast, not to a stale unicast ARP
  entry: `wakeonlan -i 192.168.1.255 <mac>`.
- Wi-Fi sender. Send from a wired host, or from a device that shares the wired
  segment.
- A firewall on the sender or on an intermediate host. A firewall on the target
  is irrelevant: the OS is off and never sees the packet.

### Wake works once, then stops

The WoL bit was cleared by a resume or by a driver reload. Keep both the
`wol-rearm.service` unit and the `system-sleep` hook installed.

## Source

- Linux kernel `r8169` driver, `Documentation/ABI` and driver source: https://github.com/torvalds/linux/tree/master/drivers/net/ethernet/realtek
- NetworkManager settings reference, `802-3-ethernet.wake-on-lan`: https://networkmanager.dev/docs/api/latest/settings-5.html
- ethtool(8) manual, `show-wol` / `wol`
- ASRock UEFI WoL option names: https://n-archives.net/software/nwol/wol-pc-setting/bios-setting-asrock.html
