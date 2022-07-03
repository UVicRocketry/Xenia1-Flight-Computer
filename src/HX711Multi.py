from ast import Or
from typing import List
import RPi.GPIO as GPIO
import numpy as np

"""

HX711_Multi: This class provides a simple way to interface with multiple
HX711 digital to analog converters connected on a single clock line.
It's intended use is for the strain gauge PCB in Xenia-1

Based on Shmulike's Arduino version https://github.com/shmulike/HX711-multi


Attributes
----------

__PD_SCK_pin [int]: GPIO pin connected to all the clocks of each HX711
(Pin 11 labeled PD_SCK in datasheet)

__DOUT_pins List[int]: GPIO pins connected to data pins of each HX711
(Pin 11 labeled DOUT in datasheet)

__gain [int]: HX711 features programmable gain settings of 64 or 128 for
channel A which is used on the strain gauge pcb. 128 is used by default. NOTE: __gain stores
the number of cycles of the PD_SCK pin needed to set the gain for the HX711. For
128, __gain = 3, for 64, __gain = 2. This is outlined in the datasheet for the
HX711.

__debug_enabled [bool]: Print debug messages to the console when True.

__num_of_HX711s [int]: Total number of HX711s based on the number of DOUT
pins passed to __init__.


Methods
-------

isReady()
    Checks if the HX711 is ready to send data. From data sheet:
        When output data is not ready for retrieval:
        - Digital output pin (DOUT) is high (5V)
        - Serial clock input (PD_SCK) should be low. 
        When ready for retrieval:
        -  DOUT goes to low (0V):

    Returns True if HX711 is ready, False otherwise.

__setGain()
    Channel A of the HX711 can be set to either 64 or 128 gain.

    Returns nothing.

__powerUp()
    Turn on the HX711s
    
    Returns nothing.
    
read_raw()
    Gets raw integer readings from all HX711s. NOTE: isReady() must return True
    before calling read_raw() or it will fail.

    Returns a list of integer readings from the HX711s if isReady(),
    otherwise returns False.

"""

class HX711_Multi:

    __PD_SCK_pin = None
    __DOUT_pins = []
    __gain = None
    __debug_enabled = None
    __num_of_HX711s = None

    def __init__(self, 
                data_pins: List[int],
                clock_pin: int,
                gain: int = 128,
                debug: bool = False):

        self.__PD_SCK_pin = clock_pin
        self.__DOUT_pins = data_pins
        self.__debug_enabled = debug
        self.__num_of_HX711s = len(self.__DOUT_pins)

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__PD_SCK_pin, GPIO.OUT)
        for pin in self.__DOUT_pins:
            GPIO.setup(pin, GPIO.IN)
            
        self.__setGain(gain)
        self.__powerUp()

    def isReady(self):

        # DOUT pin goes low (0V) when it is ready to send a reading
        for data_pin in self.__DOUT_pins:
            if GPIO.input(data_pin) == GPIO.HIGH:
                if self.__debug_enabled:
                    print("HX711 on pin", data_pin, "not ready")
                    continue
                return False
                
        return True

    def readRaw(self):

        if self.__debug_enabled and not self.isReady():
            print("HX711s are not ready! Ensure isReady() returns True",
                  "before calling readRaw()")

        # Read value from every HX711. Each cycle of PD_SCK shifts one bit
        # out in twos complement.
        readings = [0]*self.__num_of_HX711s

        for bits in range(24):

            GPIO.output(self.__PD_SCK_pin, GPIO.HIGH)
            GPIO.output(self.__PD_SCK_pin, GPIO.LOW)

            for i, data_pin in enumerate(self.__DOUT_pins):
                readings[i] = readings[i] << 1
                readings[i] |= GPIO.input(data_pin)

        # Gain for the next reading is set by cycling the PD_SCK pin
        # __gain number of times.
        GPIO.output(self.__PD_SCK_pin, GPIO.LOW)

        for _ in range(self.__gain):
            GPIO.output(self.__PD_SCK_pin, GPIO.HIGH)
            GPIO.output(self.__PD_SCK_pin, GPIO.LOW)
            
        # Calculate int from 2's complement as this is the form the HX711
        # sends its data according to the datasheet. Readings are 24bit.
        for reading in readings:
            if (reading & (1 << (24 - 1))) != 0:
                reading = reading - (1 << 24)

        return readings

    def __powerUp(self):
        GPIO.output(self.__PD_SCK_pin, GPIO.LOW)

    def __setGain(self, gain):

        assert gain == 128 or gain == 64, "Gain must be 128 or 64!"

        if gain == 128:
            self.__gain = 1
        else:
            self.__gain = 3
