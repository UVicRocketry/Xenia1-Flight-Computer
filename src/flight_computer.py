import board

import time
from airbrakes import Airbrakes
import RPi.GPIO as GPIO
import busio
from rocketData import RocketData
import numpy as np
from camera import Camera
import subprocess

from HX711Multi import HX711_Multi

#TODO: double check all these thresholds with @jj and @morgan
STANDBY_EXIT_THRESHOLD = 10
POWERED_FLIGHT_EXIT_THRESHOLD = -9
POWERED_TIMEOUT = 5 # Claire says 3 seconds expected
COAST_TIMEOUT = 40 # Claire says 29 seconds expected
RECOVERY_TIMEOUT = 480

TIME_OF_SUSTAINED_ACCELERATION = 1.2
BLACKBOX_FILEPATH = "/media/pi/black_box/requirements.txt"

class FlightComputer:

    def __init__(self):
        self.rocket_data = RocketData()
        self.black_box = open(BLACKBOX_FILEPATH, "a")
        self.startup()

    def startup(self):
        """Initialize all the things"""
        self.__init_stepper()

        self.__config_buzzer()
        if self.rocket_data.lsm_sensor_ready():
            # lsm sensors read correctly
            self.beep()
        if self.rocket_data.bme_sensor_ready():
            # bme sensors read correctly
            self.beep()
        if self.rocket_data.adx_sensor_ready():
            # adx sensors read correctly
            self.beep()

        if not (self.rocket_data.lsm_sensor_ready() or self.rocket_data.bme_sensor_ready() or self.rocket_data.adx_sensor_ready()):
            # didnt read all sensors, not ready to go
            self.beep(1.2)


    def __init_stepper(self):
        """
        This should initialize the airbrakes stepper motor and open and close airbrakes
        The main driver for the airbrakes should automatically do this upon
        initialization.
        Don't stand next to the airbrakes at this point.
        """
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(4, GPIO.OUT)
        airbrakes = Airbrakes(direction = True)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(4, GPIO.HIGH)
        airbrakes.calibrate()


    def __config_buzzer(self):
        GPIO.setup(19, GPIO.OUT)


    def beep(self, duration = 0.2):
        """
        This method should buzz the buzzer. Different durations mean different
        things, default of 0.2 indicate success
        """
        GPIO.output(19, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(19, GPIO.LOW)


    def vec_len(self, v):
        return np.sqrt(np.dot(v, v))


    def __standby(self):
        start_of_acceleration_time = time.time()
        while True:
            self.rocket_data.refresh()
            if (self.vec_len(self.rocket_data.current_acceleration) < STANDBY_EXIT_THRESHOLD):
                #if acceleration threshold is not met, reset time threshold
                start_of_acceleration_time = time.time()
            elif (self.vec_len(self.rocket_data.current_acceleration) > STANDBY_EXIT_THRESHOLD) and ((start_of_acceleration_time + TIME_OF_SUSTAINED_ACCELERATION) < time.time()):
                #if acceleration is met and the time threshold is met, break into powered_flight
                break


    def __powered_flight(self):
        time_at_start = time.time()
        while True:
            self.rocket_data.refresh()
            self.rocket_data.send_to_black_box(self.black_box)
            if time.time() > (time_at_start + POWERED_TIMEOUT):
                break
            elif self.rocket_data.current_acceleration < POWERED_FLIGHT_EXIT_THRESHOLD:
                break


    def __coast_flight(self):
        time_at_start = time.time()

        while True:
            self.rocket_data.refresh()
            self.rocket_data.send_to_black_box(self.black_box)
            # TODO: send data to airbrakes
            if time.time > (time_at_start + COAST_TIMEOUT):
                break
            elif self.rocket_data.velocity < 0:
                break


    def __recovery_flight(self):
        time_at_start = time.time()

        while True:
            self.rocket_data.refresh()
            self.rocket_data.send_to_black_box(self.black_box)
            if time.time > (time_at_start + RECOVERY_TIMEOUT):
                break
            elif self.rocket_data.velocity == 0:
                break


    def fly(self):
        self.__standby()
        self.__powered_flight()
        self.__coast_flight()
        self.__recovery_flight()
        self.black_box.close()
