import sys

# TODO: Uncomment these once the modules don't have errors.
# from gpioReader import GPIOReader
# from rocketData import RocketData

def initialize():
    """Initialize and setup all data.

    In this stage we should take extreme care with errors in file loading and
    such. This method should only ever fail in extreme cases.

    Params
    ------

    * `test_mode` - If true, then this method will return fake controllers.


    Returns
    -------

    The data controllers to access and control the rocket. If test_mode is set
    then these controllers will be mocked controllers that run a simulation.
    """

    # TODO: Can this fail? If so, make it not.
    # TODO: In test mode this should be fake.

    # TODO: Include gpioReader once we have a working GPIO_READER.
    # rocket_data = RocketData()
    rocket_data = None
    # TODO: For the GpioReader class, this is where a fake one would be initted.
    # gpio = GPIOReader(TEST_MODE, False, False, False, False, False, False, False)
    # gpio.retrieveData() 

    # TODO: !MC - Suborbit should be initialized in here.
    # TODO: Actually initialize everything. (Like gpio reader)

    return (rocket_data)


def standby():
    """Sitting on the rail, waiting for launch.

    The rocket may be in this state for up to 6 hours, and will not get a
    heads up before the rocket launches.

    This state should be looking and waiting for detection of motors being
    fired. We will have to detect this through means other than a direct
    signal (Something like a large acceleration spike).

    If possible, only one sensor should be active to conserve power. This will
    most likely be some sort of accelerometer. Aila will have more information
    on what sensor should be used here.

    Once launch is detected, this method will return.
    """
    # TODO: Implement this state
    pass


def powered_flight():
    """This is when the rocket motor is actively firing.

    This should only last around three seconds.

    The flight computer should stay in this state until either we detect motor
    burnout, or a manual limit is reached (such as 5s)

    During this stage there should be **no airbrakes**
    """
    # TODO: Implement this state
    pass


def coast_flight():
    """This is when the rocket is still moving upwards to apogee, but after
    motor burnout.

    This phase will last roughly 27s.

    The flight computer should stay in this state until either we detect apogee,
    or a manual limit is reached (such as 45s).

    This state will be responsible for Airbrakes!
    """
    # TODO: Implement this state
    # TODO: This is where we will have to deal with threading for the airbrakes
    #       controls.
    pass


def recovery():
    """This is the final state after apogee.

    This phase is of unknown length (to Mateo. Should ask around to confirm.).

    The flight computer should stay in this state until recovered. This is
    forever as far as the FC is concerned.
    """
    # TODO: Implement this state
    pass


def main():
    """Main loop of the program.

    This is where most of the magic happens and where all states are controlled.
    """

    # This is the initialization state
    (rocket_data) = initialize()

    # At this point we are sitting on the rail and waiting for a detection of
    # motor ignition.
    standby()

    # These are the in-flight stages.
    powered_flight()
    coast_flight()
    recovery()

    # And that's a wrap.
    print("Thank you for flying Air Xenia. Hope you enjoyed your flight.")


def process_cli_args():
    """Process the supplied command line arguments.


    Flags
    -----

    * `--test` or `-t` : Run the program is test mode.


    Returns
    -------

    The return values is a struct of (boolean), where the first element is
    whether or not to run in test mode.
    """
    test_mode = False

    for (i, arg) in enumerate(sys.argv):
        if i == 0:
            continue

        if arg == "--test" or arg == "-t":
            test_mode = True
        else:
            # NOTE: We explicitely DO NOT fail here because this is a rocket.
            #       An incorrect argument is not a reason to fail completely.
            print("Warning: Unkown argument supplied: ", arg)

    return (test_mode)


if __name__ == "__main__":
    (test_mode) = process_cli_args()

    global TEST_MODE
    TEST_MODE = test_mode

    main()
    exit(0)
