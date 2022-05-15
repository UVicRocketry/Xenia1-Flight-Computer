
'''
This is the original developed script for recording a video on the camera, tested and works
from time import sleep
from picamera import PiCamera
camera = PiCamera()
camera.resolution = (1024, 760)
camera.start_preview()
camera.start_recording('video.h264')
sleep(5)
camera.stop_recording()
camera.stop_preview()
'''


#This is the draft for the camera stream 

import io
import random
import picamera

def motion_detected():
    # Randomly return True (like a fake motion detection routine)
    return random.randint(0, 10) == 0

camera = picamera.PiCamera()
stream = picamera.PiCameraCircularIO(camera, seconds=20)
camera.start_recording(stream, format='h264')
try:
    while True:
        camera.wait_recording(1)
        if motion_detected():
            # Keep recording for 10 seconds and only then write the
            # stream to disk
            camera.wait_recording(10)
            stream.copy_to('motion.h264')
finally:
    camera.stop_recording()