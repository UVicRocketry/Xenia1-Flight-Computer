from time import sleep
from picamera import PiCamera
from src.flight_computer import BLACKBOX_FILEPATH

CAMERA_RESOLUTION = (1024, 760)
RECORDING_TIME = 1000
BLACKBOX_FILEPATH = '/media/black_box/'

camera = PiCamera()
camera.resolution = CAMERA_RESOLUTION

camera.start_recording(BLACKBOX_FILEPATH)
sleep(RECORDING_TIME)
camera.stop_recording()
