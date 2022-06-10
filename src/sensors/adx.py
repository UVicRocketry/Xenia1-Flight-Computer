import adafruit_adxl37x

class Adx:

    __adxl375 = None

    acceleration = None

    def __init__(self):
        self.__adxl375 = adafruit_adxl37x.ADXL375(i2c)
    
    @property
    def acceleration(self):
        return self.__read_unsafe() or self.acceleration

    def __read_unsafe(self):
        try:
            self.acceleration = self.__adxl375.acceleration
            return self.acceleration
        except:
            return None
    


