import board

import time
from airbrakes import Airbrakes
import RPi.GPIO as GPIO
import busio
from rocketData import RocketData
import numpy as np

from HX711Multi import HX711_Multi


STANDBY_EXIT_THRESHOLD = 10
POWERED_FLIGHT_EXIT_THRESHOLD = -9
POWERED_TIMEOUT = 5
COAST_TIMEOUT = 300
RECOVERY_TIMEOUT = 480

# TODO: complete filepath
BLACKBOX_FILEPATH = "/media/pi/XENIA_BB"

class FlightComputer:

    def __init__(self):
        self.rocket_data = RocketData()
        self.f = open(BLACKBOX_FILEPATH, "a")
        self.startup()

    def startup(self):
        """Initialize all the things"""
        self.__init_stepper()
    
        self.__config_buzzer()
        if self.rocket_data.test_lsm_sensor_readings():
            # lsm sensors read correctly
            self.__beep()
        if self.rocket_data.test_bme_sensor_readings():
            # bme sensors read correctly
            self.__beep()
        if self.rocket_data.test_adx_sensor_readings():
            # adx sensors read correctly
            self.__beep()
        
        if not (self.rocket_data.test_lsm_sensor_readings() or self.rocket_data.test_bme_sensor_readings() or self.rocket_data.test_adx_sensor_readings()):
            # didnt read all sensors, not ready to go
            self.__beep(1.2)
            

    def __init_stepper():
        """
        This should initialize the airbrakes stepper motor and open and close airbrakes
        The main driver for the airbrakes should automatically do this upon
        initialization.
        Don't stand next to the airbrakes at this point.
        """

        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(4, GPIO.OUT)
        airbrakes = Airbrakes(direction = True)
        # GPIO.setmode(GPIO.BOARD)
        # Set the pins as outputs
        GPIO.output(18, GPIO.LOW)
        GPIO.output(4, GPIO.HIGH)
        # This will wave at the fans (move the brakes in and out)
        airbrakes.calibrate()
        print("calibrate")

    def __config_buzzer():
        GPIO.setup(19, GPIO.OUT)

    def __beep(duration = 0.2):
        """This method should buzz the buzzer to let the operator know that setup
        is complete."""
        GPIO.output(19, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(19, GPIO.LOW)


    def __standby(self):
        while True:
            self.rocket_data.refresh()
            if self.vec_len(self.rocket_data.acceleration) < STANDBY_EXIT_THRESHOLD:
                break
    
    def vec_len(v):
        return np.sqrt(np.dot(v, v))

    def __powered_flight(self):
        time_at_start = time.time()
        
        while True:
            self.rocket_data.refresh()
            self.rocket_data.send_to_blackbox()
            # TODO: send data to airbrakes
            if time.time() > (time_at_start + POWERED_TIMEOUT):
                break
            elif self.rocket_data.current_acceleration < POWERED_FLIGHT_EXIT_THRESHOLD:
                break

    def __coast_flight(self):
        time_at_start = time.time()
        
        while True:
            self.rocket_data.refresh()
            self.rocket_data.send_to_blackbox()
            # TODO: send data to airbrakes
            if time.time > (time_at_start + COAST_TIMEOUT):
                break
            elif self.rocket_data.velocity < 0:
                break
        
    def __recovery_flight(self):
        time_at_start = time.time()
        
        while True:
            self.rocket_data.refresh()
            self.rocket_data.send_to_blackbox()
            if time.time > (time_at_start + RECOVERY_TIMEOUT):
                break
            elif self.rocketdata.velocity == 0:
                break

    def fly(self):
        self.__standby()
        self.__powered_flight()
        self.__coast_flight()
        self.__recovery_flight()
        self.f.close()
