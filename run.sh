#!/bin/bash
docker run --privileged=true --rm -h KernelDev -e DISPLAY=:0 -v /home/intel/workspace/:/root/workspace -it clayding/kerneldeploymentplat
