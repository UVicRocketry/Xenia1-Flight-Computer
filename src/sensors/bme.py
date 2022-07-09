import board
from adafruit_bme280 import basic as adafruit_bme280
from safe_value import SafeValue

"""
    refresh(): reads new values from all sensors on chip and stores the data. If the data is not critical to calculations it is stored in
    a variable. If it is critical it is stored in a SafeValue object. The variables are named after what is measured. for example,
    __altitude stores the acceleration SafeValue object.

    @property getters: Returns the latest value stored in the variable or the SafeValue Object. If the specific value is flight critical
    (for example altitude) there is getters for acceleration which returns non-null values regardless of if sensor is functioning
    and acceleration_unsafe which returns exactly what the sensor read.

    __read_/.../_unsafe(): Reads the sensor and returns sensor value or None if read was unsuccessful
"""

def __altitude_backup():
    # TODO complete this function
    pass

class Bme: 

    __bme280 = None

    __temperature = None
    __humidity = None
    __pressure = None
    __altitude = SafeValue([0, 10000], __altitude_backup)


    def __init__(self):
        i2c = board.I2C()
        self.__bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        self.__bme280.sea_level_pressure = 1013.25
        # the datasheet lists this as a generic value, but we should get an accurate one before launch
        # TODO: initialize pins (from wiring diagram)

    def refresh(self):
        self.__humidity = self.__read_humidity_unsafe()
        self.__pressure = self.__read_pressure_unsafe()
        self.__temperature = self.__read_temperature_unsafe()
        self.__altitude.update(self.__read_altitude_unsafe())

    @property
    def humidity(self):
        return self.__humidity

    def __read_humidity_unsafe(self): 
        try: 
            return self.__bme280.humidity
        except:
            return None

    @property
    def pressure(self):
        return self.__pressure

    def __read_pressure_unsafe(self): 
        try: 
            return self.__bme280.pressure
        except:
            return None
    
    @property
    def temperature(self):
        return self.__temperature

    def __read_temperature_unsafe(self):
        #attempt to read sensor and return None if unsuccessful
        try: 
            return self.__bme280.temperature
        except:
            return None

    @property
    def altitude(self):
        return self.__altitude.get_last_safe_value()

    @property
    def altitude_unsafe(self):
        return self.__altitude.get_last_unsafe_value()

    def __read_altitude_unsafe(self):
        try: 
            return self.__bme280.altitude
        except:
            return None