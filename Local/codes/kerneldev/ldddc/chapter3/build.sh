#########################################################################
# File Name: build.sh
# Author: Shikun Ding
# mail:shikun.ding@intel.com
# Created Time: Wed Mar 10 06:23:05 2021
#########################################################################
#!/bin/bash
#make CFLAGS="-Wall -O2" chrdev_test
arm-linux-gnueabihf-gcc -Wall -O2 chrdev_test.c -o chrdev_test