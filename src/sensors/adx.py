import adafruit_adxl37x
from safe_value import SafeValue


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

    refresh(): reads new values from all sensors on chip and stores the data. If the data is not critical to calculations it is stored in
    a variable. If it is critical it is stored in a SafeValue object. The variables are named after what is measured. for example,
    __acceleration stores the acceleration SafeValue object.

    @property getters: Returns the latest value stored in the variable or the SafeValue Object. If the specific value is flight critical
    (for example acceleration) there is getters for acceleration which returns non-null values regardless of if sensor is functioning
    and acceleration_unsafe which returns exactly what the sensor read.

    __read_/.../_unsafe(): Reads the sensor and returns sensor value or None if read was unsuccessful  

    """

    __adxl375 = None

    __acceleration = SafeValue([-100,100],-9.8)

    def __init__(self):
        i2c = board.I2C()
        self.__adxl375 = adafruit_adxl37x.ADXL375(i2c)
    
    def refresh(self):
        #gets new data from sensors and uses update() function in safe_value class to place data in last_value and last_safe_value
        self.__acceleration.update(self.__read_acceleration_unsafe())
    
    @property
    def acceleration(self):
        #returns last safe value or result of alternative function if the sensor has returned None for longer than the TIMEOUT setting.
        return self.__acceleration.get_last_safe_value()

    @property
    def acceleration_unsafe(self):
        #returns the last unsafe value but does not update object.
        return self.__acceleration.get_last_unsafe_value()

    def __read_acceleration_unsafe(self):
        try:
            return self.__adxl375.acceleration
        except:
            return None
