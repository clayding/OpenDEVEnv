# docker4kernel


### Quick Start
1. Locate the python3
   ```
   $ whereis python3
    python3: /usr/bin/python3 /usr/bin/python3.8-config /usr/bin/python3.8 /usr/lib/python3 /usr/lib/python3.8 /usr/lib/python3.9 /etc/python3 /etc/python3.8 /usr/local/lib/python3.8 /usr/include/python3.8 /usr/share/python3 /usr/share/man/man1/python3.1.gz
   ```
2. Install pip and depenencies:
   ```
   $ sudo apt install python3-pip
   
   $ pip3 install jinjia2
   ```
3. Print help message
   ```
   $ ./setup --help
    usage: setup [-h] [-b BUILDIR] [-c ...] [-d] [-g] [-n NAME] [-k] [-m MOUNT] [-p PROXY] [-s] [-t TAG] [-v VERBOSE]

    optional arguments:
      -h, --help            show this help message and exit
      -b BUILDIR, --buildir BUILDIR
                            set build directory path
      -c ..., --command ...
                            append command to docker run
      -d, --distclean       clean all
      -g, --generate        generate Dockerfile only, not build image
      -n NAME, --name NAME  set hostname in container
      -k, --kernel          generate Dockerfile for Kernel
      -m MOUNT, --mount MOUNT
                            mount host directories to conatiner
      -p PROXY, --proxy PROXY
                            set the http proxy to build image
      -s, --stage           build docker images in split stages
      -t TAG, --tag TAG     tag name of docker images to build
      -v VERBOSE, --verbose VERBOSE
                            set debug level to show message in run-time( debug:0, note:1, warn:2, default:1)
   ```
4. Build kernel images
   ```
   $ ./setup -k -t docker4dev_kernel -v 0 -b ./
    Create new symbol link to:././Dockerfiles/temp/Dockerfile.1638695133
    ERROR: subprocess.CalledProcessError, ignorable!!
    NOTE: Building docker builder image... (This may take some time.)

   $ ./setup -k -t docker4dev_kernel -m /home/clay/workspace/ -b ./
   ```
5. Build lede images
   ```
   $ ./setup -l -t docker4dev_lede -v 0 -b ./
    Create new symbol link to:././Dockerfiles/temp/Dockerfile.1638695133
    ERROR: subprocess.CalledProcessError, ignorable!!
    NOTE: Building docker builder image... (This may take some time.)

   $ ./setup - -t docker4dev_lede -m /home/clay/workspace/ -b ./
   ```
