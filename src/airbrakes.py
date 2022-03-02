#this is to be imported into main and constructed with rocket_data object
from pydoc import doc
import RPi.GPIO as GPIO
from time import sleep

"""
This class implements a Kalman filter to determine how far the airbrakes
flaps should be deployed, based on sensor data and previous flight data.


Attributes
----------



Methods
-------




"""
class KalmanFilter:
  def __init__(self, rd):
    rocket_data = rd



"""
This class provides a simple way to interface with the airbrakes hardware.
It is used by the KalmanFilter class.


Attributes
----------



Methods
-------




"""
class Airbrakes:
  
  # Set when calibrate() is called
  __max_pot_val = None
  __min_pot_val = None

  def __init__(self, potentiometer_pin, stepper_pin, direction_pin,
               direction: bool, step_angle=1.8, microsteps=16,
               step_delay_micro_sec=75, gear_box_ratio=14):

    # GPIO pins
    self.pot_pin = potentiometer_pin
    self.step_pin = stepper_pin
    self.dir_pin  = direction_pin

    # Stepper motor specs
    self.motor_direction: bool = direction
    self.step_delay = step_delay_micro_sec/1000000.0
    self.step_angle = step_angle
    self.microsteps = microsteps
    self.gear_ratio = gear_box_ratio
   
    # Max steps to go from fully closed to fully open with 1.25 FoS
    # Division by 6 is because airbrakes only require 1/6 of a turn to open
    self.__max_steps_to_open = 1.25*(self.gear_ratio*(360/self.step_angle)*self.microsteps)/(6)

    # Use numbering that appears on PCB
    GPIO.setmode(GPIO.BOARD)

    # Set the pins as outputs
    GPIO.setup(self.step_pin, GPIO.OUT)
    GPIO.setup(self.dir_pin, GPIO.OUT)

  def __singleStep(self, step_direction: bool):

    # ^ XORs the direction (inverting it if motor_direction dictates it)
    GPIO.output(self.dir_pin, step_direction ^ self.motor_direction)

    GPIO.output(self.step_pin, GPIO.HIGH)
    sleep(self.step_delay)
    GPIO.output(self.step_pin, GPIO.LOW)

  def deployBrakesPercent(self, percent):

    # TODO get the value of the potentiometer

    # Convert percent to potentiometer value
    #pot_value = ADC.read() or something
    target_pot = (percent/100)*(self.__max_pot_val-self.__min_pot_val)
    
    steps = 0
    while steps < self.__max_steps_to_open:
      

    








