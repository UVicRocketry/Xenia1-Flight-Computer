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
    | ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i - -b:v 65536K git_history.mp4

echo -e "${YELLOW}Converting the output to a better video codec...${PLAIN}"
ffmpeg -i git_history.mp4 \
       -c:v libx264 \
       -crf 20 \
       -profile:v baseline \
       -level 3.0 \
       -pix_fmt yuv420p \
       -movflags faststart \
       git_history.mp4

echo -e "${YELLOW}Shrinking that mp4 by reducing the quality...${PLAIN}"
ffmpeg -i git_history.mp4 -vcodec libx264 -crf 23 git_history_small.mp4

echo -e "${BLUE}Done exporting the video${PLAIN}"

echo -e "There should not be two videos in the current directory: ${BLUE}'git_history.mp4'${PLAIN} and ${BLUE}'git_history_small.mp4'${PLAIN}"
echo "The second one is just a slightly more compress version that you can post to things like Discord."

