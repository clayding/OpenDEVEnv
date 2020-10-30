#!/bin/bash


#gid=27
#uid=1000

# create a group with a proper id, in case it doesn't exist
#if ! cat /etc/group | grep ":$gid:" > /dev/null 2>&1 ; then
    #groupadd -g $gid mec
#fi

# Add uid, gid for mec, in case it doesn't exist
#if ! cat /etc/passwd | grep ":$uid:" > /dev/null 2>&1 ; then
    #useradd -m -u $uid -g $gid -s /bin/bash mec
#fi

# Use bash as the default shell
#ln -sf /bin/bash /bin/sh

#echo "MEC_SERVER" > /etc/hostname

# Zap the password for mec
#[ -e /etc/shadow ] && sed -i 's%^mec:.:%mec::%' /etc/shadow
#[ -e /etc/passwd ] && sed -i 's%^mec:x:%mec::%' /etc/passwd

#echo -e "\n# Mec privilege specification\nmec ALL=NOPASSWD: ALL" >> /etc/sudoers

#[ -c "$(tty)" ] && chmod a+rw $(tty)

#su - mec

MYUSER=root
echo "source /opt/scripts/setupvars.sh" >> /root/.bashrc
cp /opt/scripts/.vimrc /root/
su - ${MYUSER}

