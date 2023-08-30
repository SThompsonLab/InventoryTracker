#!/usr/bin/env bash

# 
# OSX, by default, does not set PWD to the directory
# in which the script lives. 
#
# So, CD to the script's directory, so we can find 
# the .inventory.csv BLIS requires 
# which should be a symlink to the shared file on the server
#
# ACTUALLY, BLIS now creates a lock file, so rather than going to 
# the local install directory (which has only the test .inventory.csv, 
# and no shared lock file), we will run with CWD set to the shared
# network drive, so users can see each other's lock files
#
cd $(dirname $0)

SHARED_DISK=/Volumes/Thompson-Lab$/Drop/BLIS

if [ ! -e "$SHARED_DISK" ]; then 
	echo " "
	echo '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
	echo '!!! ERROR: $SHARED_DISK not connected: VPN and mount fileshare  !!!'
	echo '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
	echo " "
	exit 1
fi

# 
# move to shared location
#
cd $SHARED_DISK

#
# run the correct exe for the CPU type
#
exec ./BLIS.osx.$(uname -p)


