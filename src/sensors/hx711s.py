from operator import truediv
from HX711Multi import HX711_Multi
import time


'''
Constants
'''
CLK1 = 24
CLK2 = 25
CLK3 = 12

GAIN = 128
DEBUGGER_MODE = False

DATA_PINS = [
    [ 22, 10, 9, 11 ],
    [ 5, 6, 13, 19 ],
    [ 26, 17, 27, 25 ]
]

class FakeHx711:
    """
    this class is only used in the case that an error is thrown. To make sure the error wont
    end execution of the program the class fakes the HX711 driver.
    """
    def __init__(self) -> None:
        pass


    def __get_readings():
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

class Hx711:
    """
    An Interface for HX711s

    ...

    Attributes
    ----------
    hx711s : list
        list of all hx


    Methods
    -------
    get_offsets() : [float]

    get_readings() : [float]

    """
    def __init__(self):
        self.backup_hx711 = FakeHx711()
        try:
            self.__hx1 = HX711_Multi(DATA_PINS[0], CLK1)
            self.__hx2 = HX711_Multi(DATA_PINS[1], CLK2)
            self.__hx3 = HX711_Multi(DATA_PINS[2], CLK3)
            self.hx711s = [self.__hx1, self.__hx2, self.__hx3]
        except:
            self.hx711s = self.backup_hx711


    def get_offsets(self):
        for i in range(10):
            self.__get_readings()

        return self.__get_readings()


    def __get_readings(self):
        readings = []

        for hx in self.hx711s:

            while not hx.isReady():
                time.sleep(0.005)

            values = hx.readRaw()

            for value in values:
                readings.append(value)

        return readings


    def refresh(self):
        self.__get_readings()
