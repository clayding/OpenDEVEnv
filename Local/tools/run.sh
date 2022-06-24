#!/bin/bash
docker run --privileged=true --rm -h KernelDev -e DISPLAY=:0 -v /home/intel/Workspace/:/root/workspace -it clayding/kerneldeploymentplat
