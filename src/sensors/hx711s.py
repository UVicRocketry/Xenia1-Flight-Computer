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

class Hx711:
    """
    An Interface for HX711s

    ...

    Attributes
    ----------
    hx711s : list


    Methods
    -------
    get_offsets() : [float]

    get_readings() : [float]

    """


    def __init__(self):
        self.__hx1 = HX711_Multi(DATA_PINS[0], CLK1)
        self.__hx2 = HX711_Multi(DATA_PINS[1], CLK2)
        self.__hx3 = HX711_Multi(DATA_PINS[2], CLK3)
        self.hx711s = [self.__hx1, self.__hx2, self.__hx3]


    def get_offsets(self):
        for i in range(10):
            self.get_readings()

        return self.get_readings()


    def get_readings(self):
        readings = []

        for hx in self.hx711s:

            while not hx.isReady():
                time.sleep(0.005)

            values = hx.readRaw()

            for value in values:
                readings.append(value)

        return readings
