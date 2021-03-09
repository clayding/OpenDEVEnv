#########################################################################
# File Name: qemu_start.sh
# Author: Shikun Ding
# mail:shikun.ding@intel.com
# Created Time: Thu Feb 25 13:54:18 2021
#########################################################################
#!/bin/bash
qemu-system-arm \
    -M vexpress-a9 -m 1024M \
    -kernel /root/linux/arch/arm/boot/zImage \
    -append "rdinit=/linuxrc console=ttyAMA0 loglevel=8" \
    -dtb /root/linux/arch/arm/boot/dts/vexpress-v2p-ca9.dtb \
    --fsdev local,id=kmod_dev,path=/opt/shared,security_model=none \
    -device virtio-9p-device,fsdev=kmod_dev,mount_tag=share_mount\
    -netdev user,id=mynet\
    -device virtio-net-device,netdev=mynet\
    -nographic

# Mount share dir in emulated env:
# mkdir -p /mnt/host_share && mount -t 9p -o trans=virtio share_mount /mnt/host_share -oversion=9p2000.L
