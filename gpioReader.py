#!/usr/bin/env python

from time import sleep
import RPi.GPIO as GPIO
##pip3 install gpiozero
##import gpiozero as gpio

# research needed
# Reading input
# have to install library on pi
class GPIOReader():

    ## PIN CONSTANTS
    PINS = {
        "PIN_CONST" = (4)
    }

    ## Private Method for seting up variables and inputs on pins
    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_CONST, GPIO.IN)
        return

    ## Private Method for reading an individual pins value (either pin is high: 1 or low: 0)
    def __readPin(self, pin):
        return GPIO.input(pin)

    def __cleanUp(self):
        GPIO.cleanup()
        return

    ## Public Method to be called externally to grab data from sensors
    def retrieveData(self):
        for pin in PINS:
            input_value = __readPin(PINS[pin])
            print


    def __init__(self):

        ## INITIALIZE PINS
        setup()

    
    
