FROM ubuntu:18.04
MAINTAINER clayding<gdskclay@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get clean && apt-get update && apt-get upgrade -y --fix-missing
RUN apt-get update && apt-get install -y  git vim cmake sudo libsdl2-dev nasm yasm libboost-all-dev libgflags-dev libgoogle-glog-dev protobuf-compiler libhdf5-dev libatlas-base-dev lsb-core ethtool quilt autoconf linux-headers-4.15.0-46-generic tk flex pciutils libnl-route-3-200 graphviz tcl chrpath kmod automake swig lsof dpatch bison net-tools inetutils-ping wget
RUN apt-get install -y qemu libncurses5-dev gcc-arm-linux-gnueabi build-essential gcc-5-arm-linux-gnueabi

ENV SCRDIR=/opt/scripts
ENV PACDIR=/opt/packages

COPY ./scripts/  $SCRDIR
COPY ./packages  $PACDIR
RUN chmod +x $SCRDIR/*
RUN $SCRDIR/deploymentinit.sh

ENTRYPOINT ["bash", "/opt/scripts/start.sh"]
