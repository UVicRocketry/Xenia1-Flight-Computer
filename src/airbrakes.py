#this is to be imported into main and constructed with rocket_data object
from pydoc import doc
import RPi.GPIO as GPIO
from time import sleep

# These libraries are required for the ADS1115 ADC
# pip install Adafruit-Blinka
# pip install adafruit-circuitpython-ads1x15
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


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

Airbrakes: This class provides a simple way to interface with the airbrakes
hardware. It is used by the KalmanFilter class.


Attributes
----------

__max_pot_val [double]: Value of the potentiometer as read by the ADC when brakes are
fully deployed. Set by calibrate().

__min_pot_val [double]: Value of the potentiometer as read by the ADC when brakes are
fully closed. Set by calibrate().

pot_pin [int]: ADS1115 pin that is connected to potentiometer
step_pin [int]: GPIO pin that controls stepping of A4988 stepper driver
dir_pin [int]: GPIO pin that controls direction of A4988 stepper driver

motor_direction [bool]: This value is XOR'd with the direction passed to
__singleStep(). For the user, this means if the flaps are opening in the wrong
direction when testing, invert the value of motor_direction.

step_delay [int]: Delay in seconds between pulses of step_pin
step_angle [int]: Step angle in degrees of stepper motor
microsteps [int]: 2 (half), 4 (quarter), 16 (sixteenth) etc.
gear_ratio [int]: (# of motor turns) / (# of gearbox output turns)

__max_steps_to_open [int]: Maximum number of steps needed to fully open the brakes.
This is calculated from the motor parameters: step_angle, microsteps, gear_ratio


Methods
-------

__singleStep():
  Steps Airbrakes stepper motor once in specified direction.

  Returns nothing.

  Param: step_direction
    Passing step_direction=True opens Airbrakes one step
    Passing step_direction=False closes Airbrakes one step

    Note: If passing True closes Airbrakes, invert the value of 
    step_direction when initializing Airbrakes object

calibrate(): 
  Sets __max_pot_val by reading potentiometer in the fully open state
  and sets __min_pot_val by reading the potentiometer in the closed state

  Returns nothing.

  Must be called before launch (on the launch pad) to calibrate the system.

deployBrakes():
  Opens the brakes to the specifed percentage of fully open.

  Returns value of potentiometer at final position.

  Note: This uses the potentiometer for feedback so there will be a small
  error associated with this. Adjust this error by changing max_error in
  method body.


"""
class Airbrakes:
  
  # Set when calibrate() is called
  __max_pot_val = None
  __min_pot_val = None

  def __init__(self,
              stepper_pin,
              direction_pin, 
              direction: bool,
              ads_pot_pin=0,
              step_angle=1.8,
              microsteps=16,
              step_delay_micro_sec=75,
              gear_box_ratio=14):

    # GPIO pins
    self.step_pin = stepper_pin
    self.dir_pin  = direction_pin

    # Stepper motor specs
    self.stepper_motor = {
      "direction": bool(direction),
      "step_delay": step_delay_micro_sec/1000000.0,
      "step_angle": step_angle,
      "microsteps": microsteps,
      "gear_ratio": gear_box_ratio
    }
   
    # Max steps to go from fully closed to fully open with 1.25 safety factor 
    # Division by 6 is because airbrakes only require 1/6 of a turn to open
    self.__max_steps_to_open = (1.25
                                * (self.stepper_motor["gear_ratio"]
                                   *(360/self.stepper_motor["step_angle"])
                                   * self.stepper_motor["microsteps"])
                                /6)

    GPIO.setmode(GPIO.BOARD)

    # Set the pins as outputs
    GPIO.setup(self.step_pin, GPIO.OUT)
    GPIO.setup(self.dir_pin, GPIO.OUT)

    # Initialize ADC (ADS1115) for reading the potentiometer 
    self.i2c = busio.I2C(board.SCL, board.SDA)
    self.ads = ADS.ADS1115(self.i2c)
    self.potentiometer = AnalogIn(self.ads, ads_pot_pin)

  def __singleStep(self, step_direction: bool):

    # ^ XORs the direction (inverting it if motor_direction dictates it)
    GPIO.output(self.dir_pin, step_direction ^ self.stepper_motor["direction"])

    # Pulse step pin (raise to 5V, then lower to 0V) to step the motor
    # For most stepper drivers the recommended pulse time is 5 microseconds
    # but 7 seems to work a bit smoother.
    GPIO.output(self.step_pin, GPIO.HIGH)
    sleep(7e-6)
    GPIO.output(self.step_pin, GPIO.LOW)
    sleep(self.stepper_motor["step_delay"] - 7e-6)

  def calibrate(self):
    
    # Fully open brakes and record pot value
    for _ in range(self.__max_steps_to_open):
      self.__singleStep(True)
    self.__max_pot_val = self.potentiometer.value

    # Fully close brakes and record pot value
    for _ in range(self.__max_steps_to_open):
      self.__singleStep(False)
    self.__min_pot_val = self.potentiometer.value

  def deployBrakes(self, percent):

    # Convert percent to potentiometer value
    target_pot = self.__min_pot_val + (percent/100)*(self.__max_pot_val-self.__min_pot_val)
    
    curr_error = target_pot-self.potentiometer.value

    # TODO set this based on the resolution of ADC/pot, slop in gears, etc. (requires testing)
    max_error  = 10 

    # Move stepper to target position within some error
    # Prevent infinite loop by never stepping more than the max to open
    steps = 0
    while abs(curr_error) > max_error and steps < self.__max_steps_to_open:
      
      if curr_error < 0:
        self.__singleStep(True)
      else:
        self.__singleStep(False)

      curr_error = target_pot - self.potentiometer.value
      steps += 1
    
    # Return the final potentiometer value
    return self.potentiometer.value
