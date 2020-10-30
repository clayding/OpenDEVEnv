#!/bin/bash

# active environment
source $SCRDIR/setupvars.sh

KERNELVER=linux-4.0.1
BUSYBOXVER=busybox-1.32.0
COMPILER=gcc-linaro-5.5.0-2017.10-x86_64_arm-linux-gnueabihf

KERNELBALL=$PACDIR/linux-4.0.1.tar.gz
BUSYBOXBALL=$PACDIR/busybox-1.32.0.tar.bz2
COMPILERBALL=$PACDIR/gcc-linaro-5.5.0-2017.10-x86_64_arm-linux-gnueabihf.tar.xz

KERNELURL=https://mirrors.edge.kernel.org/pub/linux/kernel/v4.x/${KERNELVER}.tar.gz
BUSYBOXURL=https://busybox.net/downloads/${BUSYBOXVER}.tar.bz2
COMPILERURL=https://releases.linaro.org/components/toolchain/binaries/latest-5/arm-linux-gnueabihf/$COMPILER.tar.xz

CONFIGDIR=$PACDIR/config/
KERNELCONF=$CONFIGDIR/kernel_config
BUSYBOXCONF=$CONFIGDIR/busybox_config

DEVDIR=/opt/devspace
KERNELSRC=$DEVDIR/$KERNELVER/
BUSYBOXSRC=$DEVDIR/$BUSYBOXVER/

# Download linux kernel and busybox from internet
if [ ! -f $KERNELBALL ];then
    echo "Download linux kernel from $KERNELURL"
    wget -c $KERNELURL -P $PACDIR
fi

if [ ! -f $BUSYBOXBALL ];then
    echo "Download busybox from $BUSYBOXURL"
    wget -c $BUSYBOXURL -P $PACDIR
fi

echo ${COMPILERBALL}
if [ ! -f ${COMPILERBALL} ];then
    echo "Download arm compiler from $COMPILERURL"
    wget -c $COMPILERURL -P $PACDIR
fi

if [ ! -d $DEVDIR ];then
    echo "Creating $DEVDIR as development space"
    mkdir -p $DEVDIR
else
    rm $DEVDIR/* -r
fi

# Uncompress tarballs
echo "Untar $KERNELBALL $DEVDIR"
tar xzf $KERNELBALL -C $DEVDIR

echo "Untar $BUSYBOXBALL to $DEVDIR"
tar xjf $BUSYBOXBALL -C $DEVDIR

echo "Untar $COMPILERBALL to $DEVDIR"
tar xf ${COMPILERBALL} -C $DEVDIR

# Config arm linux compiler
COMPILERBIN=$DEVDIR/${COMPILER}/bin
NEWPATH=`echo $PATH | sed  "s|COMPILERPATH|$COMPILERBIN|g"`

# Replace COMPILERPATH by the path of compiler
sed -i "s|COMPILERPATH|$COMPILERBIN|g" $SCRDIR/setupvars.sh
export PATH=${NEWPATH}

# Compile busybox
cd $BUSYBOXSRC  && make defconfig
cp $BUSYBOXCONF $BUSYBOXSRC/.config
make -j8 && make install

# Complete rootfs
cd _install/
mkdir etc dev mnt
mkdir etc/init.d/

# Edit init.d/rcS
tee etc/init.d/rcS <<-'EOF'
mkdir -p /proc
mkdir -p /tmp
mkdir -p /sys
mkdir -p /mnt
/bin/mount -a
mkdir -p /dev/pts
mount -t devpts devpts /dev/pts
echo /sbin/mdev > /proc/sys/kernel/hotplug
mdev -s
EOF

chmod +x  etc/init.d/rcS

tee etc/fstab <<-'EOF'
proc                    /proc                   proc    defaults        0 0                                                                                                                                                                                                                                                                                           
tmpfs                   /tmp                    tmpfs   defaults        0 0 
sysfs                   /sys                    sysfs   defaults        0 0 
tmpfs                   /dev                    tmpfs   defaults        0 0 
debugfs                 /sys/kernel/debug       debugfs defaults        0 0 
EOF

cd dev/
sudo mknod console c 5 1
sudo mknod null  c 1 3

# Compile linux kernel
cp -r $BUSYBOXSRC/_install/ $KERNELSRC
cd $KERNELSRC && make vexpress_defconfig
echo "Copy kernel configuration file from $KERNELCONF to $KERNELSRC"
cp $KERNELCONF $KERNELSRC/.config

make bzImage -j8
make dtbs

# Create a sympol link for kernel source
ln -s $KERNELSRC /root/linux
