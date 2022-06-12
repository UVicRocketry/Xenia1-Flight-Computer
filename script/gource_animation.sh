#!/bin/bash

# This script takes the entire git history and turns it into a video using a
# utility called 'gource'
#
# To run the script you must install gource and ffmpeg, and run this script
# from the base of the repo.
#
# Script created by Mateo Carreras, June 2022


#
# Constants
#

# These are color constants that will give certain messages colour to them
YELLOW='\033[0;33m'
BLUE='\033[0;36m'
RED='\033[0;31m'
PLAIN='\033[0m'


#
# Error handling
#

# This command makes the script exit if any of the commands return an error code
set -e

#
# Video Generation
#

echo -e "${YELLOW}Generating the video...${PLAIN}"
gource -s 0.1 \
       --key \
       -1920x1080 \
       --auto-skip-seconds 0.1\
       --multi-sampling \
       --hide mouse,filenames \
       --file-idle-time 0 \
       --max-files 0 \
       --bloom-multiplier 2.0 \
       --title "UVR Xenia Git Repo" \
       --logo ./script/uvr_logo.png \
       --stop-at-end \
       --output-ppm-stream - \
       --output-framerate 60 \
    | ffmpeg -y -r 60 \
             -f image2pipe \
             -vcodec ppm \
             -i - \
             -vcodec libx264 \
             -preset medium \
             -pix_fmt yuv420p \
             -crf 23 \
             -threads 0 \
             -bf 0 \
             git_history.mp4

echo -e "${BLUE}Done exporting the video${PLAIN}"
echo -e "There should not be a video in the current directory: ${BLUE}'git_history.mp4'${PLAIN}"

