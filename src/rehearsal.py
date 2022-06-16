# Rehearsal script
#
# This script is meant to be run during the assembly rehearsal instead of main
# that will do the things with the sensors.
#
# MOST LOGIC SHOULD BE IN THE MAIN CODE. In theory, this should be only calling
# functions and controlling the flow.

from airbrakes import Airbrakes

def startup():
    """Initialize all the things"""
    init_stepper()
    tare_hx711s()
    config_i2c()


def init_stepper():
    """This should initialize the airbrakes stepper motor and open and close airbrakes

    The main driver for the airbrakes should automatically do this upon
    initialization.

    Don't stand next to the airbrakes at this point."""

    # TODO: I have ZERO idea what this direction should be. There is a 50%
    #       chance that this is correct.
    airbrakes = Airbrakes(direction = True)

    # This will wave at the fans (move the brakes in and out)
    airbrakes.calibrate()


def tare_hx711s():
    """Basically like zeroing a scale, but with the strain gauges"""
    pass


def config_i2c():
    """Setup all sensors with i2c and setup."""
    pass


def gather_data():
    """Collect data once and return."""
    pass


def transmit_data(data):
    """Send data through transmitter once."""
    pass


def rehearsal():
    startup()

    while True:
        # TODO: I don't know what this data needs to be.
        data = gather_data()
        transmit_data(data)
