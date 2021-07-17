
#similar to a json object 

class SensorDataObject:
    def __init__(self):
        self.bme = {
           "humidity": 0,
           "temperature": 0,
           "pressure": 0 
        }
        self.imu = {
            "yaw": 0,
            "pitch": 0,
            "roll": 0,
            "linear_acceleration": 0,
            "linear_velocity": 0
        }
        #https://docs.google.com/document/d/1gTJJ3SIZ1-oAkT5Fk1SbSard9b0-FxJ6s4E3crWBEo4/edit
        # strian 
        self.strain_gauges = {
            "one": 0,
            "two": 0,
            "three": 0,
			"four": 0,
			"five": 0, 
			"six": 0,
			"seven": 0,
			"eight": 0,
			"nine": 0,
			"ten": 0,
			"eleven": 0,
			"twelve": 0,
			"thirteen": 0  
        }
        self.encoders = {
            "position": 0
        }

        self.time = 0; 

    def self.set_bme(self,humdity, temperature,pressure):
        return

    def self.set_imu():
        return

    def self.set_strain_gauges():
        return

    def self.convert_to_csv():
        return
    
    

