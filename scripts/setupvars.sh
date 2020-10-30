#!/bin/bash

if [ ! $PACDIR ]; then
        export PACDIR=/opt/packages
fi

if [ ! $SCRDIR ]; then
	export SCRDIR=/opt/scripts
fi

if [ ! $CODDIR ]; then
	export CODDIR=/opt/codes
fi

SELFSCRIPT=$SCRDIR/
EXISTED=$(echo $PATH | grep "SELFSCRIPT")	
if [ ! $EXISTED ]; then	
	export PATH=$SELFSCRIPT:$PATH
fi

export ARCH=arm
export CROSS_COMPILE=arm-linux-gnueabihf-
export PATH=$PATH:###COMPILERPATH###
export KERNELDIR=###KERNELPATH###
export CODESDIR=###CODESPATH###

echo "[setupvars.sh] environment initialized"
