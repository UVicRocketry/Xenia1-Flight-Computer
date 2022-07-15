import adafruit_adxl34x

class Adx:
    """
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

    refresh(): reads new values from all sensors on chip and stores the data.

    @property getters: Returns the latest value stored in the variable.

    __read_/.../(): Reads the sensor and returns sensor value or None if read was unsuccessful  

    """

    __adxl375 = None

    __acceleration = None

    def __init__(self):
        i2c = board.I2C()
        self.__adxl375 = adafruit_adxl34x.ADXL345(i2c)
    
    def refresh(self):
        #gets new data from sensors and uses update() function in safe_value class to place data in last_value and last_safe_value
        self.__acceleration = self.__read_acceleration()
    
    @property
    def acceleration(self):
        #returns last safe value or result of alternative function if the sensor has returned None for longer than the TIMEOUT setting.
        return self.__acceleration.get_last_safe_value()

    def __read_acceleration(self):
        try:
            return self.__adxl375.acceleration
        except:
            return None
