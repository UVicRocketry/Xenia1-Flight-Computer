import adafruit_adxl37x
import board

class Adx:
    """
    Adx sensor object

    ...

    Attributes
    ----------

    __adxl375 : object
        Driver for adx sensor, holds methods
        for each sensor value

    acceleration : float
        Temperature value from the bme280

    Methods
    -------

    read_unsafe_x() : float or None
        Tries to return a sensor value reading
        if the value doesn't read returns None

    """
    __adxl375 = None

    acceleration = None

    def __init__(self):
        i2c = board.I2C()
        self.__adxl375 = adafruit_adxl37x.ADXL375(i2c)
        # TODO: initialize pins (from wiring diagram)

    @property
    def acceleration(self):
        return self.__read_unsafe() or self.acceleration

    def __read_unsafe_acceleration(self):
        try:
            self.acceleration = self.__adxl375.acceleration
            return self.acceleration
        except:
            return None
