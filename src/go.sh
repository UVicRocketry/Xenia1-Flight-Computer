#!/bin/bash

echo "STARTING FLIGHT COMPUTER $(date +%s-%H:%M:%S)"

python3 camera.py &
sudo python3 /home/pi/Xenia1-flight-Computer/src/main.py
