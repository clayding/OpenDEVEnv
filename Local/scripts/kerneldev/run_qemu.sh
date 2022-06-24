#!/bin/bash
qemu-system-arm -M vexpress-a9 -smp 4 -m 100M -kernel $KERNELDIR/arch/arm/boot/zImage \
-dtb $KERNELDIR/arch/arm/boot/dts/vexpress-v2p-ca9.dtb -nographic \
-append "rdinit=/linuxrc console=ttyAMA0 loglevel=8 slub_debug kmemleak=on" \
--fsdev local,id=kmod_dev,path=$CODESDIR,security_model=none -device virtio-9p-device,fsdev=kmod_dev,mount_tag=kmod_mount \
$DBG

