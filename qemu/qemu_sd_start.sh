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
    -append "root=/dev/mmcblk0 rw rdinit=/linuxrc console=ttyAMA0 loglevel=8" \
    -dtb /root/linux/arch/arm/boot/dts/vexpress-v2p-ca9.dtb \
    -sd /root/workspace/kernelvolumes/rootfs.ext3 \
    -nographic
