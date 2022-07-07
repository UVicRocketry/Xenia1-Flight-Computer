import board
from adafruit_bme280 import basic as adafruit_bme280

class bme:

    """
    bme sensor object

    ...

    Attributes
    ----------

    __bme280 : object
        Driver for bme sensor, holds methods
        for each sensor value

    temperature : float
        Temperature value from the bme280

    humidity : float
        Humidity value from the bme280

    pressure : float
        Pressure value from the bme280

    Methods
    -------

    read_unsafe_x() : float or None
        Tries to return a sensor value reading
        if the value doesn't read returns None

    """


    __bme280 = None

    temperature = None
    humidity = None
    pressure = None
    altitude = None

    def __init__(self):
        i2c = board.I2C()
        self.__bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        self.__bme280.sea_level_pressure = 1013.25
        # the datasheet lists this as a generic value, but we should get an accurate one before launch

        # TODO: initialize pins (from wiring diagram)

    @property
    def humidity(self):
        return self.read_unsafe_humidity() or self.humidity

    def read_unsafe_humidity(self):
        try:
            self.humidity = self.__bme280.humidity
            return self.humidity
        except:
            return None

    @property
    def pressure(self):
        return self.read_unsafe_pressure or self.pressure

    def read_unsafe_pressure(self):
        try:
            self.pressure = self.__bme280.pressure
            return self.pressure
        except:
            return None
    @property
    def temperature(self):
        return self.read_unsafe_temperature() or self.temperature

    def read_unsafe_temperature(self):
        try:
            self.temperature = self.__bme280.temperature
            return self.temperature
        except:
            return None

    def altitude(self):
        return self.read_unsafe_altitude() or self.altitude

    def read_unsafe_altitude(self):
        try:
            self.altitude = self.__bme280.altitude
            return self.altitude
        except:
            return None
