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
    _encoders = None

    def __init__(self):
        self._bme = Bme()
        self._lsm = Lsm()
        self._adx = Adx()
        self._encoders = Encoder() #there's no encoder class right now

        self.data = {
            # this might need to be restructured depending on how the sensor classes are done
            'bme temperature': self._bme.read_temperature(),
            'bme pressure': self._bme.read_pressure(),
            'bme humidity': self._bme.read_humidity(),
            'bme altitude': self._bme.read_altitude(),

            'lsm temperature': self._lsm.read_temperature(),
            'lsm acceleration': self._lsm.read_acceleration(),
            'lsm gyroscope': self._lsm.read_gyroscope(),
            'lsm magnetometer': self._lsm.read_magnetometer(),

            'adx acceleration': self._adx.read_acceleration(),

            'strain gauges': [
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
            'encoder': self._encoders,
            'timestamp': float
        }


    @property
    def data(self):
        return self.data


    @property
    def time_stamp(self):
        return self.data['time_stamp']

    @time_stamp.setter
    def time_stamp(self, ts):
        self.data['time_stamp'] = ts


    # Set all sensor data -> get rid of this or make it an update all values function? shouldn't need to manually set data
    @data.setter
    def setdata(self, vals):

    def all_rocketdata(self):
        all_data = [
            self.data['bme temperature'],
            self.data['bme pressure'],
            self.data['bme humidity'],
            self.data['bme altitude'],
            self.data['lsm temperature'],
            self.data['lsm acceleration'],
            self.data['lsm gyroscope'],
            self.data['lsm magnetometer'],
            self.data['adx acceleration'],
            self.data['strain gauges'][0],
            self.data['strain gauges'][1],
            self.data['strain gauges'][2],
            self.data['strain gauges'][3],
            self.data['strain gauges'][4],
            self.data['strain gauges'][5],
            self.data['strain gauges'][6],
            self.data['strain gauges'][7],
            self.data['strain gauges'][8],
            self.data['strain gauges'][9],
            self.data['strain gauges'][10],
            self.data['strain gauges'][11],
            self.data['encoders']['position'],
            self.data['encoders']['percent'],
            self.data['timestamp'],
        ]
        return all_data

    def convert_to_csv_string(self):
        data_to_convert = self.all_rocketdata()
        csv_string = str(data_to_convert[0])
        for data in data_to_convert[1:]:
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

    def send_to_ground():
        # TODO: get a string of critical data to send to groundstation
        #       - what data are we actually sending to ground?
        #       - how is it going to be formatted? (200c string but does it need to be
        #         human readable?)
