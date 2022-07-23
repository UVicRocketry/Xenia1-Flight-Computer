import picamera

CAMERA_RESOLUTION = (1024, 760)
RECORDING_TIME = 60 * 20
BLACKBOX_FILEPATH = '/media/black_box/video.h264'

with picamera.PiCamera() as camera:
    camera.resolution = CAMERA_RESOLUTION

    camera.start_recording(BLACKBOX_FILEPATH)
    camera.wait_recording(RECORDING_TIME)
    camera.stop_recording()
