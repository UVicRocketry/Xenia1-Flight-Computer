import board

import time
from airbrakes import Airbrakes
import RPi.GPIO as GPIO
import busio
from rocketData import RocketData
import numpy as np
import suborbit

from HX711Multi import HX711_Multi

# Gees required to exit standby. This G load must be sustained for a certain time
# TODO CHECK THESE WITH CLAIRE AND FIGURE OUT IF THEY ARE IN G or m/s
STANDBY_ACCELERATION_THRESHOLD = 3*9.81
POWERED_FLIGHT_EXIT_THRESHOLD = -9

# Motor burn time is 3s according to data sheet.
POWERED_TIMEOUT = 3*1.15

#  From flight dynamics.
COAST_TIMEOUT = 300

# Under parachute from max apogee of 14000ft, the rocket takes 310s to descend.
RECOVERY_TIMEOUT = 310*1.5
BUZZ_PIN = 21

# BLACKBOX_FILEPATH = "/media/pi/black_box"
BLACKBOX_FILEPATH = "/media/black_box/flight_data_" + str(time.strftime("%H-%M-%S")) + ".txt"

def mach(n):
    return 339.0 * n

class FlightComputer:
    def __init__(self):
        print("initting the FC")
        self.rocket_data = RocketData()

        print("Attempting to open file")
        self.black_box = open(BLACKBOX_FILEPATH , "a+")


        print("Suborbit")
        self.suborbit = suborbit.Suborbit()

        print("Airbrakes")
        self.airbrakes = Airbrakes(False, 8, 4, 7)

        print("Startup")
        self.startup()
        print("Seatbelt sign is on (FC is initialized)")


    def startup(self):
        """Initialize all the things"""

        print("Sensor roll call\n  buzzer")
        self.__config_buzzer()
        self.beep(duration = 1) 
        time.sleep(5)

        if self.rocket_data.lsm_sensor_ready():
            # lsm sensors read correctly
            print("  lsm init successfully")
        else:
            self.beep(count = 1)
            time.sleep(3.0)
            print("  lsm failed to init")

        if self.rocket_data.bme_sensor_ready():
            # bme sensors read correctly
            print("  bme init successfully")
        else:
            self.beep(count = 2)
            time.sleep(3.0)
            print("  bme failed to init")

        if self.rocket_data.adx_sensor_ready():
            # adx sensors read correctly
            print("  adx init successfully")
        else:
            self.beep(count = 3)
            time.sleep(3.0)
            print("  adx failed to init")

        if self.airbrakes.calibrate():
            print("  airbrakes init successfully")
        else:
            self.beep(count = 4)
            time.sleep(3.0)
            print("  airbrakes failed to init")
        self.airbrakes.deployBrakes(0)
        self.beep(duration = 1) 
        time.sleep(5)

    def __config_buzzer(self):
        GPIO.setup(BUZZ_PIN, GPIO.OUT)


    def beep(self, duration = 0.2, count = 1):
        """
        This method should buzz the buzzer. Different durations mean different
        things, default of 0.2 indicate success
        """
        print("beeping", count, "times, for", duration, "seconds")
        
        return 

        for i in range(count):
            if not i is 0:
                time.sleep(duration)
            

            GPIO.output(BUZZ_PIN, GPIO.HIGH)
            time.sleep(duration)
            GPIO.output(BUZZ_PIN, GPIO.LOW)


    def vec_len(v):
        return np.sqrt(np.dot(v, v))


    def __standby(self):
        self.airbrakes.sleep()
        while True:
            print("Stnadby")
            self.rocket_data.refresh()
            self.rocket_data.send_to_black_box(self.black_box)
            current_accel = FlightComputer.vec_len(self.rocket_data.current_acceleration)
            if current_accel < STANDBY_ACCELERATION_THRESHOLD:
                timer = time.time()
                if abs(timer - time.time()) > 1:
                    break


    def __powered_flight(self):
        time_at_start = time.time()

        while True:
            print("Powered Flight")
            self.rocket_data.refresh()
            self.rocket_data.send_to_black_box(self.black_box)
            if time.time() > (time_at_start + POWERED_TIMEOUT) or self.rocket_data.current_acceleration < POWERED_FLIGHT_EXIT_THRESHOLD:
                break


    def __coast_flight(self):
        time_at_start = time.time()
        self.airbrakes.wake()
        subo = suborbit.Suborbit()


        AIRBRAKES_HOLD_TIMEOUT = 4.0

        ts = time.time()
        airbrakes_released = False

        while True:
            print("Coast flight")
            self.rocket_data.refresh()
            self.rocket_data.send_to_black_box(self.black_box)

            if not (time.time() - ts >= AIRBRAKES_HOLD_TIMEOUT or airbrakes_released):
                if (not self.rocket_data.velocity is None) and self.rocket_data.velocity < mach(0.75):
                    airbrakes_released = True
                    print("airbrakes set free because of velocity")
                continue

            if not airbrakes_released:
                airbrakes_released = True
                print("airbrakes set free because of timeout")

            self.rocket_data.airbrakes_percentage = self.airbrakes.get_position()

            alt = self.rocket_data.current_altitude
            vel = self.rocket_data.velocity
            accel = self.rocket_data.current_acceleration
            self.rocket_data.update_airbrakes_percentage(self.airbrakes.get_position())
            airbrakes = self.rocket_data.airbrakes_percentage

            (max_alt, max_time) = self.suborbit.run(alt, vel, accel, airbrakes)
            new_airbrakes_position = subo.calc_airbrakes_position(alt, max_alt, airbrakes)
            self.airbrakes.deployBrakes(new_airbrakes_position)

            if time.time() > (time_at_start + COAST_TIMEOUT) or (self.rocket_data.velocity and self.rocket_data.velocity < 0):
                break


    def __recovery_flight(self):
        time_at_start = time.time()

        while True:
            print("Recovery Flight")
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
