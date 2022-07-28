import adafruit_adxl34x


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

    refresh(): reads new values from all sensors on chip and stores the data.

    @property getters: Returns the latest value stored in the variable.

    __read_/.../(): Reads the sensor and returns sensor value or None if read was unsuccessful

    """
    INPUT_FILEPATH = './test.csv'

    __adxl375 = None

    __acceleration = None
    __input_file = None
    __input_array = None
    __y_index = 0

    def __init__(self, i2c):
        try:
            self.__adxl375 = adafruit_adxl34x.ADXL345(i2c)
            self.__input_file = open(INPUT_FILEPATH)
            self.__input_array = np.loadtxt(self.__input_file)
        except ValueError:
            self.__adxl375 = {
                'acceleration': 0
            }


    def refresh(self):
        #gets new data from sensors and uses update() function in safe_value class to place data in last_value and last_safe_value
        try:
            self.__acceleration = (self.__input_array[14][self.__y_index], self.__input_array[15][self.__y_index], self.__input_array[16][self.__y_index])
            self.__y_index += 1
        except:
            self.__acceleration = None
    
    @property
    def acceleration(self):
        #returns last safe value or result of alternative function if the sensor has returned None for longer than the TIMEOUT setting.
        return self.__acceleration

    def __read_acceleration(self):
        try:
            return self.__adxl375.acceleration
        except:
            return None
