import time
import csv
import board

from .sensors.bme import Bme
from .sensors.adx import Adx
from .sensors.lsm import Lsm
from .sensors.hx711s import Hx711

GRAVITY = 9.80665

GAS_CONSTANT = 8.3144598

ATMOSPHERIC_MOLAR_MASS = 0.289644

H2O_VAPOUR_HEAT = 2501000

SPECIFIC_GAS_DRY = 287

SPECIFIC_GAS_H2O = 461.5

SPECIFIC_HEAT_DRY_AIR = 1003.5

INITIALIZED_ALTITUDE = 274.1

LAPSE_RATE = 0.0098

ACCELERATION_DIRECTION_INDEX = 1


class RocketData():
    """
    A class to store, manipulate, and send rocket data

    ...

    Attributes
    ----------
    lsm : Object
        sensor object for lsm

    bme : Object
        sensor object for bme

    adx : Object
        sensor object for adx

    strain_gauges : Object
        sensor object for the 12 hx711s

    velocity : float
        calculated velocity

    Methods
    -------
    __all_rocket_data()
        Description: returns an array of all sensor data to be used in convert_to_csv_string

    __convert_to_csv_string()
        Description: converts all of the data into a csv string

    send_to_airbrake()
        Description: sends an object that contains altitude, velocity, and acceleration
        info to calculations, which will send it to airbrakes (idk if this is how it works
        but send_to_airbrakes will send an object with relevant info wherever it has to go)

    send_to_black_box()
        Description: converts data to a csv string to be sent to blackbox


    """
    lsm = None
    bme = None
    adx = None
    strain_gauges = None
    velocity = 0

    def __init__(self):
        i2c = board.I2C()
        self.bme = Bme(i2c)
        self.lsm = Lsm(i2c)
        self.adx = Adx(i2c)
        self.strain_gauges = Hx711()
        self.velocity = 0
        self.current_altitude = 0
        self.current_acceleration = 0
        self.timestamp = time.time()

        self.refresh()

        self.initial_pressure = self.bme.pressure
        self.initial_humidity = self.bme.humidity
        self.initial_altitude = self.bme.altitude
        self.initial_temperature = self.bme.temperature or self.lsm.temperature


    def bme_sensor_ready(self):
        return {
            self.bme.pressure and
            self.bme.humidity and
            self.bme.altitude and
            self.bme.temperature
        }


    def lsm_sensor_ready(self):
        return {
            self.lsm.acceleration and
            self.lsm.temperature and
            self.lsm.gyroscope and
            self.lsm.magnetometer
        }


    def adx_sensor_ready(self):
        return self.adx.acceleration


    def refresh(self):
        previous_altitude = self.current_altitude
        previous_timestamp = self.timestamp

        self.bme.refresh()
        self.lsm.refresh()
        self.adx.refresh()
        self.strain_gauges.refresh()
        self.timestamp = time.time()

        self.__set_altitude()

        self.__set_acceleration()

        self.velocity = self.get_velocity(
            self.current_altitude,
            previous_altitude,
            self.timestamp,
            previous_timestamp
        )


    def __set_acceleration(self):
        if self.adx.acceleration:
            #Access y direction of ADX sensor. Multiply by -1 as y is pointing down on board
            self.current_acceleration = -1* self.adx.acceleration[ACCELERATION_DIRECTION_INDEX]
        elif self.lsm.acceleration:
            #Access y direction of LSM sensor. No operations needed as y is pointing up on board
            self.current_acceleration = self.lsm.acceleration[ACCELERATION_DIRECTION_INDEX]
        else:
            #Default Acceleration in case both ADX and LSM fail
            self.current_acceleration = -1 * GRAVITY


    def __set_altitude(self):
        """
        This function updates altitude with backup values if bme stops reading altitude
        """
        if not self.bme.altitude and self.bme.pressure:
            self.current_altitude = self.altitude_barometric(self.bme.pressure, self.initial_pressure, self.initial_temperature)
        elif not self.bme.altitude and (self.bme.temperature or self.lsm.temperature):
            if self.bme.temperature:
                self.current_altitude = self.altitude_temperature(self.bme.temperature, self.initial_temperature)
            elif self.lsm.temperature:
                self.current_altitude = self.altitude_temperature(self.lsm.temperature, self.initial_temperature)


    def __all_rocket_data(self):
        if not self.adx.acceleration:
            self.adx.acceleration = (None, None, None)
        if not self.lsm.acceleration:
            self.lsm.acceleration = (None, None, None)
        if not self.lsm.gyroscope:
            self.lsm.gyroscope = (None, None, None)
        if not self.lsm.magnetometer:
            self.lsm.magnetometer = (None, None, None)
        all_data = [
            self.bme.temperature,
            self.bme.pressure,
            self.bme.humidity,
            self.bme.altitude,
            self.lsm.temperature,
            self.lsm.acceleration,
            self.lsm.gyroscope,
            self.lsm.magnetometer,
            self.adx.acceleration,
            *self.strain_gauges,
            self.timestamp,
        ]
        return all_data


    def convert_to_csv_string(self):
        data_to_convert = self.__all_rocket_data()
        csv_string = ""
        for data in data_to_convert[0:]:
            if data is None:
                csv_string += ","
            else:
                csv_string += "," + str(data)

        return csv_string


    def airbrakes_data(altitude, velocity, acceleration, init_altitude):
        init_altitude = init_altitude or None
        return init_altitude, altitude, velocity, acceleration


    def send_to_black_box(self, black_box):
        """
        Writes rocket data to a file on the black box
        Parameters:
            black_box: string, the directory of blackbox on the pi should be something like '/media/pi/...'

        Returns: None

        """
        writer = csv.writer(black_box)
        writer.writerow(self.convert_to_csv_string())


    def get_velocity(self, current_alt, prev_alt, current_timestamp, prev_timestamp):
        if current_alt != type(None) and prev_alt != type(None):
            dh = current_alt - prev_alt
            dt = current_timestamp - prev_timestamp
            return dh/dt
            # TODO Ensure that dt is never 0
        else:
            return None


    def initialize_lapse_rate(moist, pressure, temperature):
        """
        Takes moistness, pressure, and temperature readings at launch site to find lapse rate.
        This should not be run after the initialization phase

        Parameters:
            moist: float, water vapour pressure
            pressure: float, pressure reading
            temperature: float, temperature reading

        Returns:
            lapse_rate: float, lapse rate (... duh)
        """
        numerator_numerator = H2O_VAPOUR_HEAT * moist
        numerator_denominator = temperature * SPECIFIC_GAS_H2O * (pressure - moist)

        numerator = GRAVITY * (1 + (numerator_numerator/numerator_denominator))

        denominator_numerator = H2O_VAPOUR_HEAT**2 * SPECIFIC_GAS_DRY * moist
        denominator_denominator = (SPECIFIC_GAS_H2O * temperature)**2 * (pressure - moist)

        denominator = SPECIFIC_HEAT_DRY_AIR + (denominator_numerator/denominator_denominator)

        lapse_rate = (numerator/denominator)

        return lapse_rate


    def altitude_barometric(pressure, init_pressure, init_temperature):
        """
        Takes pressure reading, initial pressure reading, and initial temperature reading to get altitude

        Parameters:
            pressure: float, current pressure reading
            init_pressure: float, initialized pressure reading, should not change after initialization
            init_temperature: float, initialized temperature reading, should not change after initialization

        Returns:
            alt_baro: float, altitude from barometric pressure
        """

        if type(pressure) != None:
            exponent = (-1 * GAS_CONSTANT * LAPSE_RATE) / (GRAVITY * ATMOSPHERIC_MOLAR_MASS)
            pressure_component = (pressure / init_pressure)**exponent

            alt_baro = (pressure_component * init_temperature / LAPSE_RATE) + INITIALIZED_ALTITUDE - init_temperature

        elif type(pressure) == None:
            alt_baro = None

        return alt_baro


    def altitude_temperature(curr_temperature, init_temperature): # or altTemp if needed
        """
        Takes current temperature measurement and initialized temperature measurement change to get altitude from temperature.
        This version essentially turns the flight path into two linear directions (possibly ignore this, docstrings to be changed)

        Parameters:
            curr_temperature: float, current temperature reading
            init_temperature: float, initialized temperature, should not be altered after initialization phase

        Returns:
            alt_temperature: float, altitude from temperature
        """

        alt_temperature = -1 * ((curr_temperature - init_temperature)/LAPSE_RATE)

        return alt_temperature
