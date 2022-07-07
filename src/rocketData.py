import csv
# import sensors

class RocketData:
    """
    A class to store, manipulate, and send rocket data

    ...

    Attributes
    ----------
    data : object
        holds all sensor data and a timestamp

    Methods
    -------
    all_rocketdata
        Description: returns an array of all sensor data to be used in convert_to_csv_string

    convert_to_csv_string
        Description: converts all of the data into a csv string

    send_to_airbrakes
        Description: sends an object that contains altitude, velocity, and acceleration
        info to calculations, which will send it to airbrakes (idk if this is how it works
        but send_to_airbrakes will send an object with relevant info wherever it has to go)

    send_to_blackbox
        Description: converts data to a csv string to be sent to blackbox

    send_to_ground
        Description: takes critical data (what exactly?) and converts it to a string to be sent to the groundstation

    """
    data = {}

    _lsm = None
    _bme = None
    _adx = None

    def __init__(self):
        self._bme = Bme()
        self._lsm = Lsm()
        self._adx = Adx()

        self.data = {
            'bme': {
                'temperature': self._bme.temperature(),
                'pressure': self._bme.pressure(),
                'humidity': self._bme.humidity(),
                'altitude': self._bme.altitude(),
            },
            'lsm': {
                'temperature': self._lsm.temperature(),
                'acceleration': self._lsm.acceleration(),
                'gyroscope': self._lsm.gyroscope(),
                'magnetometer': self._lsm.magnetometer(),
            },
            'adx': {
                'acceleration': self._adx.acceleration(),
            },
            'strain_gauges': [
                float,
                float,
                float,
                float,
                float,
                float,
                float,
                float,
                float,
                float,
                float,
                float,
            ],
            'timestamp': float
        }


    @property
    def data(self):
        return self.data


    @property
    def timestamp(self):
        return self.data['timestamp']


    @timestamp.setter
    def timestamp(self, ts):
        self.data['timestamp'] = ts


    # Set all sensor data -> get rid of this or make it an update all values function? shouldn't need to manually set data
    @data.setter
    def set_data(self, vals):
        pass

    def all_rocketdata(self):
        all_data = [
            self.data.bme['temperature'],
            self.data.bme['pressure'],
            self.data.bme['humidity'],
            self.data.bme['altitude'],
            self.data.lsm['temperature'],
            self.data.lsm['acceleration'],
            self.data.lsm['gyroscope'],
            self.data.lsm['magnetometer'],
            self.data.adx['acceleration'],
            *self.data['strain_gauges'],
            self.data['timestamp'],
        ]
        return all_data


    def convert_to_csv_string(self):
        data_to_convert = self.all_rocketdata()
        csv_string = ""
        for data in data_to_convert[0:]:
            if data is None:
                csv_string += ","
            else:
                csv_string += "," + str(data)

        return csv_string


    def send_to_airbrakes():
        # TODO: send values to airbrakes
        #   - launch altitude (initial val)
        #   - altitude (during flight)
        #   - velocity (during flight)
        #   - acceleration (during flight)

        airbrakes_data = {
            'altitude': float, #needs to be calculated?
            'velocity': float, #needs to be calculated?
            'acceleration': float #which sensor are we getting this val from? (lsm/adx)
        }


    def send_to_blackbox():
        csv_data = convert_to_csv_string();
        # TODO: send csv_data to blackbox
