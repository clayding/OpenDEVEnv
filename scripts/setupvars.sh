#!/bin/bash

if [ ! $PACDIR ]; then
        export PACDIR=/opt/packages
fi

if [ ! $SCRDIR ]; then
	export SCRDIR=/opt/scripts
fi

SELFSCRIPT=$SCRDIR/
EXISTED=$(echo $PATH | grep "SELFSCRIPT")	
if [ ! $EXISTED ]; then	
	export PATH=$SELFSCRIPT:$PATH
fi

export ARCH=arm
export CROSS_COMPILE=arm-linux-gnueabihf-
export PATH=$PATH:COMPILERPATH

echo "[setupvars.sh] environment initialized"
