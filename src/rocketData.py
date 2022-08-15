from queue import Queue
import time
import csv
import board

from sensors.bme import Bme
from sensors.adx import Adx
from sensors.lsm import Lsm

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

VELOCITY_QUEUE_SIZE = 10


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
        velocity calculated from the average of velocity_queue


    Methods
    -------
    __all_rocket_data()
        Description: returns an array of all sensor data to be used in convert_to_csv_string

    __convert_to_csv_string()
        Description: converts all of the data into a csv string

    send_to_airbrake()
        Description: sends an object that contains altitude, velocity, and acceleration
        info to calculations, which will send it to  (idk if this is how it works
        but send_to_airbrakes will send an object with relevant info wherever it has to go)

    send_to_black_box()
        Description: converts data to a csv string to be sent to blackbox

    get_velocity() 
        Description: Takes an average of 10 altitudes and calcuates a velocity

    """
    lsm = None
    bme = None
    adx = None
    strain_gauges = None
    velocity = 0
    airbrakes_percentage = 0
    velocity_queue = []

    def __init__(self):


        i2c = board.I2C()

        self.bme = Bme(i2c)
        self.lsm = Lsm(i2c)
        self.adx = Adx(i2c)
 
        self.velocity = 0


        self.velocity_queue = []
        

        self.airbrakes_percentage = 0
 
        self.current_altitude = 0

        self.current_acceleration = 0

        self.timestamp = time.time()


        self.bme.refresh()
        self.lsm.refresh()
        self.adx.refresh()


        self.initial_pressure = self.bme.pressure or 1013.27 


        self.initial_humidity = self.bme.humidity


        self.initial_temperature = self.bme.temperature or self.lsm.temperature or 21
   
        self.refresh()
        print("Rocketdata refreshed")


    def bme_sensor_ready(self):
        return {
            self.bme.pressure and
            self.bme.humidity and
            self.bme.altitude and
            self.bme.temperature and 
            self.bme.is_error
        }


    def lsm_sensor_ready(self):
        return {
            self.lsm.acceleration and
            self.lsm.temperature and
            self.lsm.gyroscope and
            self.lsm.magnetometer and
            self.lsm.is_error
        }


    def adx_sensor_ready(self):
        return { 
            self.adx.acceleration and 
            self.adx.is_error
        }


    def update_airbrakes_percentage(self, value):
        if value:
            self.airbrakes_percentage = value


    def refresh(self):
        previous_altitude = self.current_altitude
        previous_timestamp = self.timestamp

        self.bme.refresh()

        self.lsm.refresh()

        self.adx.refresh()

        self.timestamp = time.time()

        self.__set_altitude()

        self.__set_acceleration()

        self.velocity = self.get_velocity(
            self.current_altitude,
            previous_altitude,
            self.timestamp,
            previous_timestamp
        )

        print("Finsihed Refresh")


    def __set_acceleration(self):
        if self.adx.acceleration:
            #Access y direction of ADX sensor. Multiply by -1 as y is pointing down on board
            self.current_acceleration = -1* self.adx.acceleration[ACCELERATION_DIRECTION_INDEX]
        elif self.lsm.acceleration:
            #Access y direction of LSM sensor. No operations needed as y is pointing up on board
            self.current_acceleration = self.lsm.acceleration[ACCELERATION_DIRECTION_INDEX]
        else:
            #Default Acceleration in case both ADX and LSM fail
            self.current_acceleration = -9.8


    def __set_altitude(self):
        """
        This function updates altitude with backup values if bme stops reading altitude
        """
        alt = self.bme.altitude

        if alt:
            self.current_altitude = alt
            return
        
        if not alt and self.bme.pressure:
            self.current_altitude = self.altitude_barometric(self.bme.pressure, self.initial_pressure, self.initial_temperature)
        elif not self.bme.altitude and (self.bme.temperature or self.lsm.temperature):
            if self.bme.temperature:
                self.current_altitude = self.altitude_temperature(self.bme.temperature, self.initial_temperature)
            else:
                self.current_altitude = self.altitude_temperature(self.lsm.temperature, self.initial_temperature)


    def __all_rocket_data(self):
        lsm_a = self.lsm.acceleration or (None, None, None)
        lsm_g = self.lsm.gyroscope or (None, None, None)
        lsm_m = self.lsm.magnetometer or (None, None, None)
        adx_a = self.adx.acceleration or (None, None, None)
        
        all_data = [
            self.bme.temperature,
            self.bme.pressure,
            self.bme.humidity,
            self.bme.altitude,
            self.lsm.temperature,
            *lsm_a,
            *lsm_g,
            *lsm_m,
            *adx_a,
            self.airbrakes_percentage,
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


    def send_to_black_box(self, black_box):
        """
        Writes rocket data to a file on the black box
        Parameters:
            black_box: string, the directory of blackbox on the pi should be something like '/media/pi/...'

        Returns: None

        """
        writer = csv.writer(black_box)
        writer.writerow(self.__all_rocket_data())


    def get_velocity(self, current_alt, prev_alt, current_timestamp, prev_timestamp):
        """
        Uses a queue to average data and remove outliers.
        """

        try:
            print("Trying to calc velocity,", current_alt, prev_alt, current_timestamp, prev_timestamp)
            new_velocity = (current_alt - prev_alt)/(current_timestamp - prev_timestamp)

            print("Putting it in the queue")
            print(self.velocity_queue)
            if len(self.velocity_queue) < VELOCITY_QUEUE_SIZE:
                self.velocity_queue.append(new_velocity)
            else:
                del self.velocity_queue[0]
                self.velocity_queue.append(new_velocity)
            
            print("Summing the queue")
            
            print("Velocity avg", sum(self.velocity_queue))
            return sum(self.velocity_queue) / VELOCITY_QUEUE_SIZE
            
        except:
            print("Exception in get_velo, returning None")
            return None


    def initialize_lapse_rate(self, moist, pressure, temperature):
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


    def altitude_barometric(self, pressure, init_pressure, init_temperature):
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


    def altitude_temperature(self, curr_temperature, init_temperature): # or altTemp if needed
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
