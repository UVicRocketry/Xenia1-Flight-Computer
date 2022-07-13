import time
from urllib.request import DataHandler 

from .sensors.bme import Bme
from .sensors.adx import Adx
from .sensors.lsm import Lsm
from .sensors.hx711s import Hx711

#gravitational acceleration 
GRAVITY = 9.80665

#gas constant
GAS_CONSTANT = 8.3144598

#earth atmospheric molar mass
ATMOSPHERIC_MOLAR_MASS = 0.289644

#vaporization heat of water
H2O_VAPOUR_HEAT = 2501000

#specific gas constant of dry air
SPECIFIC_GAS_DRY = 287

#specific gas constant of water vapour
SPECIFIC_GAS_H2O = 461.5

#specific heat of dry air
SPECIFIC_HEAT_DRY_AIR = 1003.5

#initialized altitude at launch pad
INITIALIZED_ALTITUDE = 274.1
# just an estimate, actual data will be collected on site

#lapse rate of the air
LAPSE_RATE = 0.0098

class RocketData():
    """
    A class to store, manipulate, and send rocket data

    ...

    Attributes
    ----------
    data : object
        holds all sensor data and a timestamp

    Methods
    -------
    all_rocket_data()
        Description: returns an array of all sensor data to be used in convert_to_csv_string

    convert_to_csv_string()
        Description: converts all of the data into a csv string

    send_to_airbrake()
        Description: sends an object that contains altitude, velocity, and acceleration
        info to calculations, which will send it to airbrakes (idk if this is how it works
        but send_to_airbrakes will send an object with relevant info wherever it has to go)

    send_to_black_box()
        Description: converts data to a csv string to be sent to blackbox

    send_to_ground()
        Description: takes critical data (what exactly?) and converts it to a string to be sent to the groundstation

    """
    _lsm = None
    _bme = None
    _adx = None
    _strain_gauges = None
    _velocity = 0

    def __init__(self):
        self._bme = Bme()
        self._lsm = Lsm()
        self._adx = Adx()
        self._strain_gauges = Hx711()
        self._velocity = 0
        self.timestamp = time.time()


    def refresh(self):
        previous_altitude = self._bme.altitude
        previous_timestamp = self.timestamp

        self._bme.refresh()
        self._lsm.refresh()
        self._adx.refresh()
        # TODO: Make HX711s refresh function
        self._strain_gauges.refresh()
        self.timestamp = time.time()
        
        self._velocity = self.get_velocity(
            self._bme.altitude, 
            previous_altitude, 
            self.timestamp, 
            previous_timestamp
        )


    def all_rocket_data(self):
        all_data = [
            self._bme.temperature,
            self._bme.pressure,
            self._bme.humidity,
            self._bme.altitude,
            self._lsm.temperature,
            self._lsm.acceleration,
            self._lsm.gyroscope,
            self._lsm.magnetometer,
            self._adx.acceleration,
            *self._strain_gauges,
            self.timestamp,
        ]
        return all_data


    def convert_to_csv_string(self):
        data_to_convert = self.all_rocket_data()
        csv_string = ""
        for data in data_to_convert[0:]:
            if data is None:
                csv_string += ","
            else:
                csv_string += "," + str(data)

        return csv_string


    def send_to_airbrakes():
        # TODO: send values to airbrakes
        #   - launch altitude (initial val)
        #   - altitude (during flight)
        #   - velocity (during flight)
        #   - acceleration (during flight)

        return {
            'altitude': float, #needs to be calculated?
            'velocity': float, #needs to be calculated?
            'acceleration': float #which sensor are we getting this val from? (lsm/adx)
        }


    def send_to_black_box(self):
        csv_data = self.convert_to_csv_string();
        # TODO: send csv_data to blackbox
        pass


    def get_velocity(current_alt, prev_alt, current_timestamp, prev_timestamp):
        if current_alt != type(None) and prev_alt != type(None):
            dh = current_alt - prev_alt
            dt = current_timestamp - prev_timestamp
            return dh/dt  
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


    def altitude_barometric(pressure, init_pressure, init_temperature): # or altBaro, if needed
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


    def altitude_temperature_v2(curr_temperature, init_temperature): # or altTemp if needed
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

