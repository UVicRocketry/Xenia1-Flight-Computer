import csv
import numpy
import functools
from collections import namedtuple

# Rocket mass in kg, including the fuel grain
ROCKET_WET_MASS = 20.3
FUEL_GRAIN_MASS = 3.423
ROCKET_DRY_MASS = ROCKET_WET_MASS - FUEL_GRAIN_MASS

# TODO: Is this needed anywhere
ROCKET_AREA = 0.011050733

# Data type for storing elements of rocket position
#
# Seems roughly equivalent a struct in other compiled languages (i.e. C, Rust)
RocketPosition = namedtuple("RocketPosition", [
    "altitude", "velocity", "acceleration"
])

# TODO: !MC - Possibly rename this because there is a class in the Xenia stuff
#       that has the same name. Maybe call this FlightData??
class DragData:
    """Storage of rocket information to be used for predictions.

    Fields
    ------
    cd_no_airbrakes_data:
      Drag coefficient with no airbrakes. Each element of the array is an array
      of mach number, cd area with power on, and cd area with no power.
    """

    def __init__(self, cd_no_airbrakes_path):
        """Initialize a new DragData object with the data specified.

        Panics
        ------
        The method will exit with status code 1 if any of the files could
        not be opened succesfully.

        Params
        ------
        cd_no_airbrakes_path:
            The path relative to program execution to the csv data for the
            coefficient of drag without airbrakes.
        """

        self.cd_no_airbrakes_data = []

        try:
            # Open the file.
            cd_no_airbrakes_file = open(cd_no_airbrakes_path, newline = '')

            cd_no_airbrakes_csv_reader = csv.reader(cd_no_airbrakes_file)
            # Store the data.
            for (i, row) in enumerate(cd_no_airbrakes_csv_reader):
                if i == 0:
                    continue
                self.cd_no_airbrakes_data.append(numpy.array(row).astype(float))

            # Close the files.
            cd_no_airbrakes_file.close()
        except:
            print("Couldn't open file")
            exit(1)

        self.cd_no_airbrakes_data.sort(key=functools.cmp_to_key(compare_drag_row))


def compare_drag_row(a, b):
    return a[0] - b[0]


def flap_area_from_degrees(degrees):
    """Get the flap area in meters squared from the degrees of opening.

    Degrees is the angle from closed in degrees, and area is in meters squared.
    """
    return -4.0e-7 * (degrees**2) + 9e-5 * degrees + 5e-5


def find_drag_coefficient(data, mach_number):
    """Binary search drag coefficient data.

    This could be accomplished with the bisect.bisect_left method in
    Python 3.10, but the Pi can only run 3.7 unless we complile from source.

    Params
    ------
    data:
      This should either be the cd_no_airbrakes_data array in a DragData object.

    mach_number:
      The desired mach number to look for.
    """
    if len(data) == 0:
        return [mach_number, 0.0, 0.0]

    if len(data) == 1:
        return data[0]

    index = int(len(data)/2)
    start = 0
    end = len(data)

    while end - start > 2:
        if data[index][0] < mach_number:
            start = index
        else:
            end = index

        index = int((end - start) / 2) + start

    return data[start]


def atmosphere(altitude):
    """Calculate the speed of sound and air density at a given altitude.

    This function is taken from atmosisa and atmoslapse functions in matlab,
    which are based on the International Standard Atmospher Model. This also
    simplifies the calculations by using standard atmospheric values. These
    values were also used in the Matlab Library.

    Params
    ------
    altitude:
      The altitude in meters.

    Returns
    -------
    The return value is a tuple[float, float]
    Where the first float is the speed of sound in meters per second,
    and the second float is the air density in kilograms per meter cubed.
    """
    # Scalar acceleration due to gravity in metere per second squared.
    gravity = 9.80665
    # Scalar specific heat ratio
    specific_heat_ratio = 1.4
    # Scalar characteristic gas constant joules per kilogram-kelvin.
    characteristic_gas_constant = 287.0531
    # Scalar lapse rate in kelvin per meter.
    lapse_rate = 0.0065
    # Height of troposphere in meters.
    troposphere_height = 11000
    # Height of tropopause in meters.
    tropopause_height = 20000
    # Air density at mean sea level in kilograms per meter cubed.
    air_density_at_sea_level = 1.225
    # Static pressure at mean sea level in pascal.
    static_pressure_at_sea_level = 101325
    # TODO: !MC - We may need this to be variable for launch day??
    # Scalar absolute temperature at mean sea level in kelvin.
    absolute_temperature_at_sea_level = 288.15

    # TODO: !MC - Replace these in the equations with the full names. These just
    #       happen to be what the matlab script used.
    h = altitude
    g = gravity
    gamma = specific_heat_ratio
    r = characteristic_gas_constant
    l = lapse_rate
    hts = troposphere_height
    htp = tropopause_height
    rho0 = air_density_at_sea_level
    p0 = static_pressure_at_sea_level
    t0 = absolute_temperature_at_sea_level
    h0 = 0

    if h > htp:
        h = htp

    if h < h0:
        h = h0

    # TODO: min function??
    h_tmp = h
    if h > hts:
        h_tmp = hts

    t = t0 - l * h_tmp

    expon = 1
    if h > hts:
        expon = numpy.exp((g / (r * t)) * (hts - h))

    a = numpy.sqrt(t * gamma * r)

    theta = t / t0

    rho = rho0 * pow(theta, (g / (l*r)) - 1.0) * expon

    return (a, rho)


def grav(alt):
    """Calculate gravity at a certain altitude in meters.

    Params
    ------
    alt:
      Altitude in meters.
    """
    # This gravity was just set based on an only estimator for
    # Cochrane Ontario, using a base elevation of 275m for ground level,
    # adding 5000ft for the middle of flight ish. The idea was that this
    # would be faster, but the benefits are negligable.
    return 9.805#(6.67408e-11 * 5.972e24) / pow((6.371e6 + alt), 2)


class Suborbit:
    def __init__(self):
        self.data = DragData("drag_data/cda_no_airbrakes.csv")


    def calc_airbrakes_position(self, estimated_alt, current_brakes):
        # TODO: Actually do the calculations
        return current_brakes

    def run(self, alt, vel, accel, airbrakes, dry_mass = ROCKET_DRY_MASS):
        """
        Calculate the height of apogee and how long until apogee.

        Params
        ------
        alt:
            Altitude in meters
        vel:
            Velocity in meters per second
        accel:
            Acceleration in meters per second per second
        airbrakes:
            The amount of airbrakes currently deployed. For example, 0.8 would
            mean that airbrakes are 80% deployed.


        Returns
        -------
        The value returned with be of type (float, float), containing the max
        altitude in meters, and the time until the rocket gets there.
        """
        initial_position = RocketPosition(alt, vel, accel)

        # Intentionally ignoring any sort of power phase because not needed.

        # This will return (float, float)
        return self.__coast(initial_position, dry_mass, airbrakes, 0.0, self.data)

    def __coast(
            self,
            initial_position,
            mass,
            airbrakes_amount,
            time,
            data
    ):
        """Rocket coasting to apogee after motor shut down.

        Params
        ------
        initial_position:
            The position of the rocket at the start of the coast phase.
        mass:
            The mass of the rocket during the coast phase.
        airbrakes_amount:
            The ratio of airbrakes to no airbrakes as a decimal. For example,
            0.8 would mean airbrakes 80% out.
        data:
            The data object that contains the drag coefficient LUT.
        """
        # TODO: !MC - Remove the data parameter and use self.data

        # Fixed dt because we are only ever using one data set.
        time_delta = 0.1
        last_position = initial_position

        while last_position.velocity > 0:

            # TODO: Use better variables than a and rho
            #       speed_of_sound and air_density
            # Calculate atmospheric conditions
            (a, rho) = atmosphere(last_position.altitude)

            # Calculate drag force.
            m_temp = last_position.velocity / a
            # TODO: !MC - When running the actual rocket, this will have to do some
            #       mixing between the airbrakes and no_airbrakes data based on the
            #       current_airbrakes position.

            # Index of one is the power off CdA
            cda_no_airbrake = find_drag_coefficient(
                data.cd_no_airbrakes_data,
                m_temp
            )[1]

            # TODO: 1.1 is constant for flap Cd, 80.0 should be the max angle of airbrakes.
            #       These should be global constants, and the max angle should be adjusted.
            # TODO: Actually just change the airbrakes_amount to airbrakes_degrees. Easier that way. And I think easier for FC to compute.
            drag_area_coefficient = cda_no_airbrake + 1.1 * flap_area_from_degrees(airbrakes_amount * 80.0)
            drag = drag_area_coefficient * 0.5 * rho * pow(last_position.velocity, 2)

            g = grav(last_position.altitude)

            accel = -drag / mass - g
            vel = last_position.acceleration * time_delta + last_position.velocity
            alt = last_position.velocity * time_delta + ((last_position.acceleration * pow(time_delta, 2)) / 2) + last_position.altitude

            # Check if we have hit the ground (Hopefully not!)
            if alt < initial_position.altitude:
                accel = 0
                vel = 0
                alt = initial_position.altitude

            last_position = RocketPosition(alt, vel, accel)

            # I'm not sure why it is going for plus one and plus two, but that was
            # what the original script did.
            time += time_delta

        return (last_position.altitude, time)


################################################################################
# Tests
#
# TODO: Move tests to own file
################################################################################

def test_data_loading():
    data = DragData("drag_data/cda_no_airbrakes.csv")

def test_running():
    so = Suborbit()

    (alt, time) = so.run(552.7, 352.45, -9.8, 0.0)
    print("alt =", alt, "time =", time)

def run_tests():
    test_data_loading()
    test_running()
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
