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

# 7 sleep, 12 enable, 24 step, 26 direction
SLEEP_PIN = 7
ENABLE_PIN = 12
STEP_PIN = 24
DIRECTION_PIN = 26

"""

Airbrakes: This class provides a simple way to interface with the airbrakes
hardware. On construction, the wake() function is called and to conserve power,
it should be put to sleep(). To call any of the functions involving movement of
the motor, Airbrakes should be (a)wake().


Attributes
----------

__max_pot_val [double]: Value of the potentiometer as read by the ADC when brakes are
fully deployed. Set by calibrate().

__min_pot_val [double]: Value of the potentiometer as read by the ADC when brakes are
fully closed. Set by calibrate().

pot_pin   [int]: ADS1115 pin that is connected to potentiometer
step_pin  [int]: GPIO pin that controls stepping of the driver 
dir_pin   [int]: GPIO pin that controls direction of the driver
sleep_pin [int]: GPIO pin that puts the driver to sleep (no holding torque)

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

  Returns value of potentiometer/percent open at final position.

  Note: This uses the potentiometer for feedback so there will be a small
  error associated with this. Adjust this error by changing max_error in
  method body.

sleep():
  Powers off the stepper motor using the sleep pin of the driver. 
  
  Returns nothing.

  Note: This means a loss of torque and thus should only be used while on the
  launch pad to save power, and NEVER during flight. It should also be used
  after the brakes have been retracted after apogee.

wake():
  Powers on the stepper motor using the sleep pin of the driver. 
  
  Returns nothing.

  Note: This means the driver is awake and powering the motor. This will consume
  a lot of power so it should only be used during flight. By default, the creating
  and Airbrakes object will call this function.

"""
class Airbrakes:
  
  # Set when calibrate() is called
  __max_pot_val = None
  __min_pot_val = None

  def __init__(self,
              direction: bool,
              stepper_pin=STEP_PIN,
              direction_pin=DIRECTION_PIN,
              sleep_pin=SLEEP_PIN,
              ads_pot_pin=0,
              step_angle=1.8,
              microsteps=16,
              step_delay_micro_sec=75,
              gear_box_ratio=14):

    # GPIO pins
    self.step_pin = stepper_pin
    self.dir_pin  = direction_pin
    self.sleep_pin= sleep_pin

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
    GPIO.setup(self.sleep_pin, GPIO.OUT)

    # Initialize ADC (ADS1115) for reading the potentiometer 
    self.i2c = busio.I2C(board.SCL, board.SDA)
    self.ads = ADS.ADS1115(self.i2c)
    self.potentiometer = AnalogIn(self.ads, ads_pot_pin)

    # Wake up the driver so that it can be calibrated by the user.
    self.wake()

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
    
    percent_deployed = ((self.potentiometer.value-self.__min_pot_val)/
              (self.__max_pot_val-self.__min_pot_val))

    # Return the final potentiometer value and percentage open
    return (self.potentiometer.value, percent_deployed)

  def sleep(self):

    # The sleep pin is active low meaning pulling it low
    # puts the driver to sleep.
    GPIO.output(self.sleep, GPIO.LOW)
  
  def wake(self):

    # The sleep pin is active low meaning pulling it high
    # powers up the driver.
    GPIO.output(self.sleep, GPIO.HIGH)