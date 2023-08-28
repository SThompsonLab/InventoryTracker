#!/usr/bin/env bash

# 
# OSX, by default, does not set PWD to the directory
# in which the script lives. 
#
# So, CD to the script's directory, so we can find 
# the .BLIS requires 
# which should be a symlink to the shared file on the server
#
cd $(dirname $0)

if [ ! -e .inventory.csv ]; then 
	echo "Linking to /Volumes/Thompson-Lab$/Drop/BLIS/.inventory.csv"
	ln -sf /Volumes/Thompson-Lab$/Drop/BLIS/.inventory.csv .
fi
exec ./BLIS


