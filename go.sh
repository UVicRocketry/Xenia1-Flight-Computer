#!/bin/bash

# go.sh
#
# Created 2022-07-12
#
# This script is meant to be the script that runs on the Raspberry Pi to start
# the flight computer systems.
#
# The script MUST be run from the base of the repo (same directory as the
# script)
#
# Currently this script doesn't do a lot, but the idea is that all someone
# ever has to do to start flight computer is run `./go.sh` and it will start.
# Also we should setup a Cron job on the Pi to run this script automatically,
# which has the benefit of anyone can change this script and it will
# automatically be used everywhere.

echo "Starting flight computer..."

# Uncomment the following line before competition
# python3 src/main.py

python3 src/rehearsal.py

echo "Thanks for flying Air Xenia!"
