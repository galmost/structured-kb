# LVM snapshots before risky agent runs (Debian 13)

Host one VG `GArk-vg`. LVs `root` (93G, ext4), `home` (LVM, ext4), `var`, `tmp`, `swap_1`. VG free ~1.8T. ext4 no btrfs/snapper. Use raw LVM snapshots. Keep 2–3 named snapshots. Snapshot cost only changed blocks (CoW). Cheap. Protect software mistakes. Disk/host loss use off-box borg backup (see backup note).

## 1. Take a snapshot before a risky run

```bash
pkexec /usr/sbin/lvcreate -L 20G -s -n root-pre-agent-$(date +%Y%m%d-%H%M) /dev/GArk-vg/root
pkexec /usr/sbin/lvs --noheadings -o lv_name,lv_size,origin /dev/GArk-vg/root-pre-agent-*   # list
```

20G plenty for one day agent churn on 32G-used root. Grow `-L` if `lvconvert` report snapshot overflow (check `lvs -o lv_attr` — `s` with `O` flag mean overflowed).

## 2. Roll back (system must be quiesced — boot a live USB if root won't mount)

```bash
pkexec /usr/sbin/lvconvert --merge /dev/GArk-vg/root-pre-agent-YYYYMMDD-HHMM   # merges on next activation
# then reboot; the merge happens during boot. Verify afterwards:
pkexec /usr/sbin/lvs   # snapshot gone, root back to snapshot content
```

## 3. Rotate: keep the last 3, delete older

```bash
# list newest-first, delete all but 3
pkexec /usr/sbin/lvs --noheadings -o lv_name /dev/GArk-vg | grep '^root-pre-agent-' | sort -r | tail -n +4 | while read s; do pkexec /usr/sbin/lvremove -y /dev/GArk-vg/$s; done
```

## 4. Do NOT rely on snapshots as backup

Snapshot live same VG. Disk failure, VG corruption, or accidental `lvremove` of origin kill both. Real recovery = gark_home git snapshots (home) + borg to NAS (everything, see backup note) + model manifest (ai/amd/avalon). Snapshot = undo button; borg = disaster recovery.

## 5. Why not Timeshift here

Timeshift on ext4 use rsync mode. Each snapshot full copy of root (~32G). 55G free on `/` only one fit. LVM snapshots give 2–3 retained for fraction of space. If system ever reinstalled on btrfs, switch to snapper/Timeshift btrfs mode for GRUB-level rollback.

## Source

- https://manpages.debian.org/lvcreate(8), lvconvert(8), lvs(8)
- https://tldp.org/HOWTO/LVM-HOWTO/snapshots_backup.html