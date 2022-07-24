import picamera

CAMERA_RESOLUTION = (1024, 760)
RECORDING_TIME = 60 * 360
BLACKBOX_FILEPATH = '/media/black_box/video.h264'

camera = picamera.PiCamera()
camera.resolution = CAMERA_RESOLUTION

camera.start_recording(BLACKBOX_FILEPATH)
camera.wait_recording(RECORDING_TIME)
camera.stop_recording()
