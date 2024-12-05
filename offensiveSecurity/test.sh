#!/bin/bash

if [ $(id -u) -ne 0 ]; then
    echo "You're not root"
    exit 1
fi

echo "You're root"
exit 0
