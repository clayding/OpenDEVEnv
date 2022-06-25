#########################################################################
# File Name: build.sh
# Author: Shikun Ding
# mail:shikun.ding@intel.com
# Created Time: Fri Feb 25 09:55:47 2022
#########################################################################
#!/bin/bash
export TOOLCHAIN=~/rpi_tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian-x64/
export CROSS_COMPILE=arm-linux-gnueabihf-
export ARCH=arm
KERNEL=kernel7
OUTPUT=$PWD/../rpi_output
export KBUILD_OUTPUT=$OUTPUT

#make bcm2709_defconfig

make zImage modules dtbs -j12

if [ $? -ne 0 ]; then
    echo -e "\n>>>>>>>>>>>>>>>>>>>>> Build Image modules dtbs failed"
    exit 1
fi
make modules_install INSTALL_MOD_PATH=$OUTPUT/modules_install

REMOTE=pi@raspberrypi:/home/pi/flash/
scp -r $OUTPUT/arch/arm/boot/ $REMOTE 2>&1 > /dev/null
MODLIB=$OUTPUT/modules_install/lib
tar -czf ${MODLIB}.tar.gz $MODLIB
scp -r ${MODLIB}.tar.gz $REMOTE 2>&1 > /dev/null

md5sum $OUTPUT/arch/arm/boot/Image
