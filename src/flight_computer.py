import board
import math
import csv
import time
from airbrakes import Airbrakes
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_lsm9ds1
import adafruit_adxl34x
import RPi.GPIO as GPIO
import busio
from rocketData import RocketData
import numpy as np

from HX711Multi import HX711_Multi

i2c = board.I2C()
# i2c = busio.I2C(board.SCL, board.SDA)

LAUNCH_ACCELERATION_THRESHOLD = 10
# TODO: complete filepath
BLACKBOX_FILEPATH = "/media/pi/.."

class FlightComputer:

    def __init__(self):
        self.rocket_data = RocketData()
        self.f = open(BLACKBOX_FILEPATH, "a")
        self.startup()

    def startup(self):
        """Initialize all the things"""
        self.init_stepper()
    
        self.config_buzzer()
        if self.config_sensors():
            self.beep()
        else:
            # didnt read all sensors not ready to go
            self.beep()
            time.sleep(0.2)
            self.beep()

    def init_stepper():
        """This should initialize the airbrakes stepper motor and open and close airbrakes
    The main driver for the airbrakes should automatically do this upon
    initialization.
    Don't stand next to the airbrakes at this point."""

        # TODO: I have ZERO idea what this direction should be. There is a 50%
        #       chance that this is correct.
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(4, GPIO.OUT)
        airbrakes = Airbrakes(direction = True)
        print("hello")

        GPIO.output(18, GPIO.LOW)
        GPIO.output(4, GPIO.HIGH)
        # This will wave at the fans (move the brakes in and out)
        airbrakes.calibrate()
        print("calibrate")

    def config_buzzer():
        # GPIO.setmode(GPIO.BOARD)
        # Set the pins as outputs
        GPIO.setup(19, GPIO.OUT)

    def config_sensors(self):
        """Test readings from sensors, returns true if all sensors read something"""
        return self.rocket_data.test_all_sensors()

    def __standby(self):
        while True:
            self.rocket_data.refresh()
            if self.vec_len(self.rocket_data.acceleration) < LAUNCH_ACCELERATION_THRESHOLD:
                break
    
    def vec_len(v):
        return np.sqrt(np.dot(v, v))

    def __powered_flight(self):
        pass

    def __coast_flight(self):
        pass

    def __recovery_flight(self);
        pass

    def fly(self):
        self.__standby()
        self.__powered_flight()
        self.__coast_flight()
        self.__recovery_flight()
        self.f.close()
