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
            # this might need to be restructured depending on how the sensor classes are done
            'bme_temperature': self._bme.temperature(),
            'bme_pressure': self._bme.pressure(),
            'bme_humidity': self._bme.humidity(),
            'bme_altitude': self._bme.altitude(),

            'lsm_temperature': self._lsm.temperature(),
            'lsm_acceleration': self._lsm.acceleration(),
            'lsm_gyroscope': self._lsm.gyroscope(),
            'lsm_magnetometer': self._lsm.magnetometer(),

            'adx_acceleration': self._adx.acceleration(),

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
            self.data['bme_temperature'],
            self.data['bme_pressure'],
            self.data['bme_humidity'],
            self.data['bme_altitude'],
            self.data['lsm_temperature'],
            self.data['lsm_acceleration'],
            self.data['lsm_gyroscope'],
            self.data['lsm_magnetometer'],
            self.data['adx_acceleration'],
            *self.data['strain_gauges'],
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
