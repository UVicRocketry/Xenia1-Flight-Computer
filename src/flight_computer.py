import board

import time
from airbrakes import Airbrakes
import RPi.GPIO as GPIO
import busio
from rocketData import RocketData
import numpy as np
import suborbit

from HX711Multi import HX711_Multi

#TODO: double check all these thresholds with @jj and @morgan
STANDBY_EXIT_THRESHOLD = 10         # G
POWERED_FLIGHT_EXIT_THRESHOLD = -9  # G
POWERED_TIMEOUT = 5                 # s
COAST_TIMEOUT = 300                 # s
RECOVERY_TIMEOUT = 480              # s
BLACKBOX_FILEPATH = "/media/pi/black_box"

class FlightComputer:

    def __init__(self):
        self.rocket_data = RocketData()
        self.black_box = open(BLACKBOX_FILEPATH, "a")
        self.suborbit = suborbit.Suborbit()
        self.airbrakes = Airbrakes()
        self.startup()

    def startup(self):
        """Initialize all the things"""
        self.__init_stepper()

        self.__config_buzzer()

        # Startup sequence
        # Missing beeps alert the user to a failed sensor
        self.beep(3)
        time.sleep(3)
        
        if self.rocket_data.lsm_sensor_ready():
            # lsm sensors read correctly
            self.beep(repetitions=1)
            time.sleep(3)

        if self.rocket_data.bme_sensor_ready():
            # bme sensors read correctly
            self.beep(repetitions=2)
            time.sleep(3)

        if self.rocket_data.adx_sensor_ready():
            # adx sensors read correctly
            self.beep(repetitions=3)
            time.sleep(3)

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


    def __config_buzzer():
        GPIO.setup(19, GPIO.OUT)


    def beep(duration = 0.2, repetitions = 1):

        for i in range(repetitions+1):
            GPIO.output(19, GPIO.HIGH)
            time.sleep(duration)
            GPIO.output(19, GPIO.LOW)
            time.sleep(0.2)

    def vec_len(v):
        return np.sqrt(np.dot(v, v))


    def __standby(self):
        while True:
            self.rocket_data.refresh()
            if self.vec_len(self.rocket_data.current_acceleration) < STANDBY_EXIT_THRESHOLD:
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

            self.rocket_data.airbrakes_percentage = self.airbrakes.get_position()
            suborbit_options = {
                'alt': self.rocket_data.current_altitude,
                'vel': self.rocket_data.velocity,
                'accel': self.rocket_data.current_acceleration,
                'airbrakes': self.rocket_data.airbrakes_percentage
            }
            (max_alt, max_time) = self.suborbit.run(suborbit_options)
            new_airbrakes_position = suborbit.calc_airbrakes_position(max_alt, current_airbrakes_position)
            self.airbrakes.deploy_airbrakes(new_airbrakes_position)

            if time.time() > (time_at_start + COAST_TIMEOUT):
                break
            elif self.rocket_data.velocity < 0:
                break


    def __recovery_flight(self):
        time_at_start = time.time()

        while True:
            self.rocket_data.refresh()
            self.rocket_data.send_to_black_box(self.black_box)
            if time.time() > (time_at_start + RECOVERY_TIMEOUT):
                break
            elif self.rocket_data.velocity == 0:
                break


    def fly(self):
        self.__standby()
        self.__powered_flight()
        self.__coast_flight()
        self.__recovery_flight()
        self.black_box.close()
