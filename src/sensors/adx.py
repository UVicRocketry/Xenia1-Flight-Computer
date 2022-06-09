import adafruit_adxl37x

class Adx:

    __adxl375 = None

    __acceleration = None

    def __init__(self):
        self.__adxl375 = adafruit_adxl37x.ADXL375(i2c)
    
    def read_acceleration(self):
        return self.__read_unsafe() or self.__acceleration

    def __read_unsafe(self):
        try:
            self.__acceleration = self.__adxl375.acceleration
            return self.__acceleration
        except:
            return None
    


