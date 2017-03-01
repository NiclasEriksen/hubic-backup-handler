#!/bin/sh
sudo apt-get install git build-essential autoconf automake libboost-system-dev libcurl4-openssl-dev libboost-filesystem-dev libboost-regex-dev libboost-program-options-dev libssl-dev
git clone https://github.com/frachop/hubic-backup.git
cd hubic-backup/
aclocal
automake
autoconf
./configure
make all
sudo cp -v src/hubic-backup /usr/local/bin/
