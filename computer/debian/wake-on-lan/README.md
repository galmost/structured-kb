# Wake-on-LAN Setup (Debian 13)

Wake-on-LAN (WoL) keep network card powered when machine sleep or off. Wake machine when receive magic packet. Magic packet is 96-byte frame. Frame has six `0xFF` bytes then target MAC address repeated sixteen times. Use it to power on headless box from another host on same LAN. No touch power button.

Two cases. Need different work:

| Wake from | Kernel state | Needs BIOS/UEFI changes |
| --- | --- | --- |
| Suspend to RAM (S3) / `freeze` | RAM powered. NIC driver armed. | No |
| Full poweroff (S5) | Board keep 5V standby on PCIe slot. | Yes |

Note cover both. Tested on Debian 13 (trixie), kernel 6.12.115+deb13.1-amd64, NetworkManager 1.52.1, `ethtool` 6.14.2, on ASRock A620I Lightning WiFi board. Realtek RTL8125 2.5GbE controller. Uses in-tree `r8169` driver.

## 0. Identify the interface, driver and MAC

Run as normal user. Nothing change state.

```bash
ip -br link
readlink /sys/class/net/enp11s0/device/driver
cat /sys/class/net/enp11s0/device/uevent
nmcli -t -f NAME,TYPE,DEVICE,STATE connection show --active
```

On test host give:

```
enp11s0          UP             9c:6b:00:34:59:d2 <BROADCAST,MULTICAST,UP,LOWER_UP>
r8169
DRIVER=r8169
PCI_ID=10EC:8125
Wired connection 1:802-3-ethernet:enp11s0:activated
```

Note interface name (`enp11s0`), connection name (`Wired connection 1`), MAC. Substitute all three below. WoL work on wired interface only. Wireless NIC not listen for magic packets when host off.

## 1. Install ethtool

Root step. Install package. `sudo` ask password in non-interactive shell. `pkexec` authenticate through polkit.

```bash
pkexec apt install -y ethtool
```

Use `sudo apt install -y ethtool` if passwordless sudo configured.

## 2. Arm WoL on the running interface

Root step. Run while link up. Some drivers reject call on down interface.

```bash
pkexec ethtool -s enp11s0 wol g
pkexec ethtool enp11s0 | grep -i wake-on
```

Expected output:

```
Wake-on: g
```

`g` mean "magic packet". Read setting also need root. Keep `pkexec` prefix on verify command.

Not survive reboot. Sections 3 to 5 make persistent.

## 3. Persist it in NetworkManager

NetworkManager 1.44+ have native per-connection WoL setting. Re-applied every time connection activates. Debian 13 ship 1.52.1. Root/polkit step:

```bash
pkexec nmcli connection modify "Wired connection 1" 802-3-ethernet.wake-on-lan magic
nmcli -f 802-3-ethernet.wake-on-lan connection show "Wired connection 1"
```

Expected output:

```
802-3-ethernet.wake-on-lan:             magic
```

Read setting work as normal user. Only `modify` need polkit.

Use `magic`, not `phy`. `phy` wake on any link-state change. Power machine on when switch port renegotiate or cable unplugged.

## 4. Re-arm at boot and during shutdown

Need for wake from poweroff. NetworkManager arm card when connection activates. But shutdown tear network down after. Driver clear WoL bit on way out. `Type=oneshot` service with `RemainAfterExit=yes` run `ExecStart` at boot and `ExecStop` late during shutdown. Card re-armed on both edges.

Root step. Write unit file into `/etc/systemd/system/`.

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

Not add `DefaultDependencies=no` to this unit. Without normal dependencies systemd not stop service on poweroff. `ExecStop` never run. Card left unarmed.

Verify:

```bash
systemctl is-enabled wol-rearm.service
systemctl is-active wol-rearm.service
```

Both must print `enabled` and `active`.

## 5. Re-arm after resume

After resume, NetworkManager re-activate connection and re-apply setting. But `system-sleep` hook cost nothing and cover case where it not. Root step:

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

Suspend work without touch firmware. Poweroff not. Board must keep standby power on PCIe slot. On ASRock boards with AMI UEFI (tested on A620I Lightning WiFi, BIOS 3.01), press `F2` at POST, enter Advanced Mode, then:

| Setting | Path | Value |
| --- | --- | --- |
| PCIE Devices Power On | Advanced → ACPI Configuration | Enabled |
| Deep Sleep | Advanced → ACPI Configuration | Disabled |

Deep Sleep (also label ErP, ErP Ready or EuPlus on other boards) must disable. It cut 5V standby to save less than one watt. Kill S5 wake. Often hide PCIe power-on option from menu.

Same options on other vendors: ASUS `Power On By PCI-E`, Gigabyte `Power On By PCI-E/PCI`, MSI `Wake on LAN` / `ErP Ready = Disabled`.

## 7. Wake the machine from another host

Install sender on any host on same LAN. `wakeonlan` send UDP magic packet and need no root:

```bash
sudo apt install -y wakeonlan        # Debian/Ubuntu
wakeonlan 9c:6b:00:34:59:d2
```

Target subnet broadcast explicitly if default not arrive:

```bash
wakeonlan -i 192.168.1.255 9c:6b:00:34:59:d2
```

`etherwake` build raw Ethernet frame instead of UDP packet. Need root. Need interface given with `-i`:

```bash
sudo apt install -y etherwake
sudo etherwake -i <sender-interface> 9c:6b:00:34:59:d2
```

With no sender installed, netcat work:

```bash
# FF*6 then MAC*16, sent to UDP port 9 on the subnet broadcast
MAC=9c:6b:00:34:59:d2
xxd -r -p <<< "ffffffffffff$(echo ${MAC//:/} | sed 's/\(..\)/\1\1\1\1\1\1\1\1\1\1\1\1\1\1\1\1/g')" \
  | nc -w1 -u -b 192.168.1.255 9
```

Test in this order. Two cases fail for different reasons:

```bash
sudo systemctl suspend      # S3: should work with only sections 1-5
sudo systemctl poweroff     # S5: needs section 6 as well
```

## Troubleshooting

### `Wake-on: d` after setting `g`

Driver reset it. Check if something else own setting:

```bash
pkexec ethtool enp11s0 | grep -i wake-on
journalctl -b -u wol-rearm.service
```

### `Cannot set new wake-on-lan settings: Operation not supported`

Interface down, or driver not expose WoL. Bring link up and retry. Confirm driver:

```bash
readlink /sys/class/net/enp11s0/device/driver
```

`r8169` support `g`. Out-of-tree vendor drivers (`r8125` from Realtek) not always. Use in-tree `r8169` on Debian 13.

### Wakes from suspend but not from poweroff

Firmware, not Linux. Confirm OS side armed. Then fix BIOS:

```bash
pkexec ethtool enp11s0 | grep -i wake-on   # must show g before poweroff
```

Disable Deep Sleep / ErP. Enable PCIE Devices Power On (section 6). Check link LEDs stay lit after poweroff. No LEDs mean no standby power. No S5 wake possible.

### Machine powers on by itself

Something other than magic packet wake it. Confirm WoL is `magic` not `phy`. Then look at other wake sources:

```bash
journalctl -b | grep -iE "wake-up|wake.*device|ACPI.*wake"
cat /sys/bus/usb/devices/*/power/wakeup 2>/dev/null | sort | uniq -c
```

Disable noisy USB device with:

```bash
echo disabled | sudo tee /sys/bus/usb/devices/<device>/power/wakeup
```

### Magic packet sent, nothing happens

Packet not reaching NIC. Most causes:

- Sender and target on different subnets. Broadcast from another subnet not cross router unless router forward directed broadcasts.
- Switch drop frame because not learned target MAC while target off. Send to subnet broadcast, not stale unicast ARP entry: `wakeonlan -i 192.168.1.255 <mac>`.
- Wi-Fi sender. Send from wired host, or device that share wired segment.
- Firewall on sender or intermediate host. Firewall on target irrelevant: OS off and never see packet.

### Wake works once, then stops

WoL bit cleared by resume or driver reload. Keep both `wol-rearm.service` unit and `system-sleep` hook installed.

## Source

- Linux kernel `r8169` driver, `Documentation/ABI` and driver source: https://github.com/torvalds/linux/tree/master/drivers/net/ethernet/realtek
- NetworkManager settings reference, `802-3-ethernet.wake-on-lan`: https://networkmanager.dev/docs/api/latest/settings-5.html
- ethtool(8) manual, `show-wol` / `wol`
- ASRock UEFI WoL option names: https://n-archives.net/software/nwol/wol-pc-setting/bios-setting-asrock.html