from HX711Multi import HX711_Multi

'''
Constants
'''

# Taring settings
NUMBER_OF_SAMPLES = 200
MAX_AWAY_FROM_STD = 0.3

# Init settings
CLK_PIN = 27
GAIN = 128
DEBUGGER_MODE = False

DATA_PIN_1 = 17
DATA_PINS = [DATA_PIN_1]


class Hx711: 
    hx711s = None
    debugger_mode = True
    readings = []
    configure = True

    def __init__(self):
        
        self.hx711s = HX711_Multi(DATA_PINS, CLK_PIN, GAIN, DEBUGGER_MODE)
        while self.configure:
            if self.hx711s.isReady():
                self.__tare()
                # TODO: Ask JJ how to get the offset reading and record the offset 
            
    
    def __tare(self):
        self.hx711s.tare(NUMBER_OF_SAMPLES, MAX_AWAY_FROM_STD)

    @property
    def hx711s(self):
        return self.__read()

    def __read(self):
        try:
            if self.hx711s.isReady():
                self.readings = self.hx711s.readRaw()
                return self.readings
        except:
            if self.debugger_mode:
                print("HX711's not ready")
            assert("HX711's not ready")

    def print_visual(self):
        '''
        Note you can't break out of this function after starting to be used for testing only 
        '''
        if self.debugger_mode:
            while True: 
                self.__read()   
                print(str(self.readings[0]) + '\n')                
