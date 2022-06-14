import board
from adafruit_bme280 import basic as adafruit_bme280

class bme:

    __bme280 = None

    __temperature = None
    __humidity = None
    __pressure = None
    altitude = None

    def __init__(self):
        i2c = board.I2C()
        self.__bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        self.__bme280.sea_level_pressure = 1013.25
        # the datasheet lists this as a generic value, but we should get an accurate one before launch

        # TODO: initialize pins (from wiring diagram)

    def read_humidity(self):
        return self.__read_unsafe_humidity() or self.__humidity

    def __read_unsafe_humidity(self):
        try:
            self.__humidity = self.__bme280.humidity
            return self.__humidity
        except:
            return None

    def read_pressure(self):
        return self.__read_unsafe_pressure() or self.__pressure

    def __read_unsafe_pressure(self):
        try:
            self.__pressure = self.__bme280.pressure
            return self.__pressure
        except:
            return None

    def read_temperature(self):
        return self.__read_unsafe_temperature() or self.__temperature

    def __read_unsafe_temperature(self):
        try:
            self.__temperature = self.__bme280.temperature
            return self.__temperature
        except:
            return None

    def altitude(self):
        return self.__read_unsafe_altitude() or self.__altitude

    def __read_unsafe_altitude(self):
        try:
            self.altitude = self.__bme280.altitude
            return self.altitude
        except:
            return None
