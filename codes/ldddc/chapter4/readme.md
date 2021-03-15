References:  
https://community.arm.com/developer/tools-software/oss-platforms/w/docs/525/device-tree

### __Compile dtc used for target(arm)__
- Enter dtc/:  
    ```
    root@KernelDev:~/workspace/kernel/docker4kernel# cd 3rdparty/dtc/
    ```

- Add these 2 lines to Makefile in root of dtc:
    ```
    CC=arm-linux-gnueabihf-gcc
    +CFLAGS=-g -Os $(SHAREDLIB_CFLAGS) -Werror $(WARNINGS) -static
    ```

- Compile:
    ```
    root@KernelDev:~/workspace/kernel/docker4kernel/3rdparty/dtc# make
    ```

- Search dynamic libraries:
    ```
    root@KernelDev:~/workspace/kernel/docker4kernel/3rdparty/dtc# arm-linux-gnueabi-readelf -d dtc
    Dynamic section at offset 0xf580 contains 24 entries:
    Tag        Type                         Name/Value
    0x00000001 (NEEDED)                     Shared library: [libc.so.6]
    ```

- To find the libc.so.6 on HOST:
    ```
    root@KernelDev:~/workspace/kernel/docker4kernel/3rdparty/dtc# find / -name libc.so.6
    /opt/devspace/gcc-linaro-5.5.0-2017.10-x86_64_arm-linux-gnueabihf/arm-linux-gnueabihf/libc/lib/libc.so.6
    ```

- Copy lib/libc.so.6 or lib/ to the target /lib, and then run:
    ```
    [arm] /mnt/host_share # ./dtc --version
    Version: DTC 1.6.0-g34d70824-dirty
    ```

### __HOST dtc tool__  
- Add dtc tool path to PATH on HOST:
    ```
    root@KernelDev:~/workspace/kernel/docker4kernel/codes/ldddc/chapter4# export PATH=/root/linux/scripts/dtc/:$PATH
    ```
- Check if it works：
    ```
    root@KernelDev:~/workspace/kernel/docker4kernel/codes/ldddc/chapter4# dtc --version
    Version: DTC 1.4.0-dirty
    ```

### __Convert DTS file into DTB binary form__

[ **Incorrect** ]  
```
root@KernelDev:~/workspace/kernel/docker4kernel/codes/ldddc/chapter4# dtc -o simple_platform.dtb simple_platform.dts


root@KernelDev:~/workspace/kernel/docker4kernel/codes/ldddc/chapter4# file simple_platform.dtb
simple_platform.dtb: ASCII text
```

[ **Correct** ]  
```
root@KernelDev:~/workspace/kernel/docker4kernel/codes/ldddc/chapter4# dtc -I dts -O dtb -o simple_platform.dtb simple_platform.dts

root@KernelDev:~/workspace/kernel/docker4kernel/codes/ldddc/chapter4# file simple_platform.dtb
simple_platform.dtb: Device Tree Blob version 17, size=1656, boot CPU=0, string block size=276, DT structure block size=1324
```
### __Revert the compilation process__
```
root@KernelDev:~/workspace/kernel/docker4kernel/codes/ldddc/chapter4# dtc -o simple_platform_reverted.dts simple_platform.dtb
```

### __Extracted DTS file from the running kernel__
```
/ # ls /proc/device-tree/
#address-cells                  memory@60000000/
#size-cells                     model
aliases/                        name
arm,hbi                         pmu/
arm,vexpress,site               scu@1e000000/
cache-controller@1e00a000/      smb/
chosen/                         timer@100e4000/
clcd@10020000/                  timer@1e000600/
compatible                      virtio_mmio@10013000/
cpus/                           virtio_mmio@10013200/
dcc/                            virtio_mmio@10013400/
interrupt-controller@1e001000/  virtio_mmio@10013600/
interrupt-parent                watchdog@100e5000/
memory-controller@100e0000/     watchdog@1e000620/
memory-controller@100e1000/

/mnt/host_share # ./dtc -I fs -o arm-running-kernel-reverted.dts /proc/device-tree

/mnt/host_share # ls
arm-running-kernel-reverted.dts  lib  dtc
```
