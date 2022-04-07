import json
from time import time


class RocketData:
    """
    A class used to represent rocket data. This only deals with manipulating the rocketdata. If you don't set everything right away you will error out

    ...

    Attributes
    ----------
    _data protected attribute that holds all the sensor rocket data

    Methods
    -------
    Each attribute of the data object has a getter and setter denoted by @property by getter and @attribute.setter for setter

    How to call a setter and getter:
    rocket_data = RocketData()
    rocket_data.time_stamp <- this gets the valus of time stamp
    rocket_data.time_stamp = 6.0 <- this Sets the value of time stamp to 6.0

    multi variable sets and set through lists:

    rocket_data.imu = [5.0,6.0,7.0] <- sets in order of temperature, humidity, pressure see definitions of setters for more info

    for setting all data use rocket_data = [imu_t, imu_h, imu_p, bme_y, bme_p, bme_r, bme_a, bme_v, sg_1, sg_2, sg_3, sg_4, sg_5, sg_6, sg_7, sg_8, sg_9, sg_10, sg_11, sg_12, e, ts]

    def data_dict_set(self, rd)
        Description:
            updates the self._data with a dictionary. Differnet from setters
            because it does it updates the whole object not just individual
            attributes
        Parm:
            rd: updated _data object.

    data_to_json()
        Desciption:
            Converts the dictionary to a Json format

    print_json_data()
        Desciption:
            prints the current state of the json to the terminal

    """
    def __init__(self):
        self._data = {
            'imu': {
                'temperature': float,
                'humidity': float,
                'pressure': float,
            },
            'bme': {
                'yaw': float,
                'pitch': float,
                'roll': float,
                'linear_acceleration': float,
                'linear_velocity': float
            },
            'strain_gauges': {
                1: float,
                2: float,
                3: float,
                4: float,
                5: float,
                6: float,
                7: float,
                8: float,
                9: float,
                10: float,
                11: float,
                12: float
            },
            'encoders': {
                'position': float
            },
            'time_stamp': float
        }

    # @property decorator makes the function below a getter
    @property
    def data(self):
        return self._data

    @property
    def imu(self):
        return self._data['imu']

    @imu.setter
    def imu(self, vals):
        t, h, p = vals
        self._data['imu']['temperature'] = t
        self._data['imu']['humidity'] = h
        self._data['imu']['pressure'] = p

    @imu.setter
    def imu_temp(self, t):
        self._data['imu']['temperature'] = t


    @property
    def bme(self):
        return self._data['bme']

    @bme.setter
    def bme(self, vals):
        y, p, r, a, v = vals
        self._data['bme']['yaw'] = y
        self._data['bme']['pitch'] = p
        self._data['bme']['roll'] = r
        self._data['bme']['linear_acceleration'] = a
        self._data['bme']['linear_velocity'] = v

    @property
    def strain_gauges(self):
        return self._data['strain_gauges']

    @strain_gauges.setter
    def strain_gauges(self, vals):
        one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve = vals
        self._data['strain_gauges'][1] = one
        self._data['strain_gauges'][2] = two
        self._data['strain_gauges'][3] = three
        self._data['strain_gauges'][4] = four
        self._data['strain_gauges'][5] = five
        self._data['strain_gauges'][6] = six
        self._data['strain_gauges'][7] = seven
        self._data['strain_gauges'][8] = eight
        self._data['strain_gauges'][9] = nine
        self._data['strain_gauges'][10] = ten
        self._data['strain_gauges'][11] = eleven
        self._data['strain_gauges'][12] = twelve

    @property
    def encoders(self):
        return self._data['encoders']['position']

    @encoders.setter
    def encoders(self, p):
        self._data['encoders']['position'] = p

    @property
    def time_stamp(self):
        return self._data['time_stamp']

    @time_stamp.setter
    def time_stamp(self, ts):
        self._data['time_stamp'] = ts

    #Set all sensor data
    @data.setter
    def set_data(self, vals):
        imu_t, imu_h, imu_p, bme_y, bme_p, bme_r, bme_a, bme_v, sg_1, sg_2, sg_3, sg_4, sg_5, sg_6, sg_7, sg_8, sg_9, sg_10, sg_11, sg_12, e, ts = vals
        print(imu_t)
        self.imu([imu_t, imu_h, imu_p])
        self.bme([bme_y, bme_p, bme_r, bme_a, bme_v])
        self.strain_gauges([sg_1, sg_2, sg_3, sg_4, sg_5, sg_6, sg_7, sg_8, sg_9, sg_10, sg_11, sg_12])
        self.encoders(e)
        self.time_stamp(ts)

    def data_dict_set(self, rd):
        self._data.update(rd)

    def data_to_json(self):
        rocketData = json.dumps(self._data, indent = 4)
        print(rocketData)
        return rocketData

    def print_json_data(self):
        jsonData = self.data_to_json(self._data)
        print(jsonData)

    def all_rocket_data(self):
        allRocketData = [
            self._data['imu']['temperature'],
            self._data['imu']['humidity'],
            self._data['imu']['pressure'],
            self._data['bme']['yaw'],
            self._data['bme']['pitch'],
            self._data['bme']['roll'],
            self._data['bme']['linear_acceleration'],
            self._data['bme']['linear_velocity'],
            self._data['strain_gauges'][1],
            self._data['strain_gauges'][2],
            self._data['strain_gauges'][3],
            self._data['strain_gauges'][4],
            self._data['strain_gauges'][5],
            self._data['strain_gauges'][6],
            self._data['strain_gauges'][7],
            self._data['strain_gauges'][8],
            self._data['strain_gauges'][9],
            self._data['strain_gauges'][10],
            self._data['strain_gauges'][11],
            self._data['strain_gauges'][12],
            self._data['encoders']['position'],
            self._data['time_stamp']
        ]
        return allRocketData

    def convert_to_csv_string(self):
        dToConvert = self.all_rocket_data()
        csvString = str(dToConvert[0])
        for d in dToConvert[1:]:
            csvString += "," + str(d)

        return csvString

    #TODO: convert json data to format that antenna needs
    def convert_antenna_format(self):
        jsonData = self.data_to_json()
