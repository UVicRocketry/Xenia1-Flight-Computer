import csv
import json

#helper classes - these are used to create objects to be set in rocketData

class Bme:
    """
    bme sensor object

    ...

    Attributes
    ----------

    acceleration_x : float 
        acceleration in the x direction

    acceleration_y : float
        humidity in _ units

    acceleration_z : float 
        temperature in _ units

    """
    temperature = float
    humidity = float
    pressure = float
    bme = {}

    def __init__(self, t, h, p):
        self.temperature = t
        self.humidity = h
        self.pressure = p
        self.bme = {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure
        }
    
    def __getattribute__(self, bme: object) -> object:
        pass
        
#TODO: add units
class Lsm: 
    """
    lsm sensor object

    ...

    Attributes 
    ----------

    acceleration_x : float 
        acceleration in the x direction

    acceleration_y : float
        acceleration in the y direction

    acceleration_z : float 
        acceleration in the z direction

    magnetometer_x : float
        magnetometer in the x direction

    magnetometer_y : float
        magnetometer in the y direction

    magnetometer_z : float
        magnetometer in the z direction

    gyroscope_x : float
        gyroscope in the x direction

    gyroscope_y : float
        gyroscope in the y direction

    gyroscope_z : float
        gyroscope in the z direction

    temperature : float
        temperature in _ units TODO: what units are we reading?
    
    __lsm : object
        object that holds all the readings

    """
    acceleration_x = float
    acceleration_y = float
    acceleration_z = float
    magnetometer_x = float
    magnetometer_y = float
    magnetometer_z = float
    gyroscope_x = float
    gyroscope_y = float
    gyroscope_z = float
    temperature = float
    lsm = {}
    
    def __init__(self, ax, ay, az, mx, my, mz, gx, gy, gz, t):
        self.acceleration_x = ax
        self.acceleration_y = ay
        self.acceleration_z = az
        self.magnetometer_x = mx
        self.magnetometer_y = my
        self.magnetometer_z = mz
        self.gyroscope_x = gx
        self.gyroscope_y = gy
        self.gyroscope_z = gz
        self.temperature = t
        self.lsm = {
            'acceleration_x': self.acceleration_x,
            'acceleration_y': self.acceleration_y,
            'acceleration_z': self.acceleration_z,
            'magnetometer_x': self.magnetometer_x,
            'magnetometer_y': self.magnetometer_y,
            'magnetoneter_z': self.magnetometer_z,
            'gyroscope_x': self.gyroscope_x,
            'gyroscope_y': self.gyroscope_y,
            'gyroscope_z': self.gyroscope_z,
            'temperature': self.temperature
        }

    def __getattribute__(self, lsm: object) -> object:
        pass
    
class Encoder: 
    """
    lsm sensor object

    ...

    Attributes TODO: add units
    ----------

    position : float 
        current position reading of the encoder

    percent : float
        current percent reading of the encdoder
    
    __encoder : object

    """
    position = float
    percent = float
    encoder = {}
    
    def __init__(self, pos, per):
        self.position = pos
        self.percent = per
        self.encoder = {
            'position': self.position,
            'percent': self.percent
        }
    
    def __getattribute__(self, encoder: object) -> object:
        pass

class RocketData:
    """
    A class used to represent rocket data. This only deals with manipulating the rocketdata. If you don't set everything right away you will error out

    ...

    Attributes
    ----------
    data protected attribute that holds all the sensor rocket data

    Methods
    -------
    Each attribute of the data object has a getter and setter denoted by @property by getter and @attribute.setter for setter

    How to call a setter and getter:
    rocketdata = RocketData()
    rocketdata.time_stamp <- this gets the valus of time stamp
    rocketdata.time_stamp = 6.0 <- this Sets the value of time stamp to 6.0

    multi variable sets and set through lists:

    rocketdata.imu = [5.0,6.0,7.0] <- sets in order of temperature, humidity, pressure see definitions of setters for more info

    for setting all data use rocketdata = [imu_t, imu_h, imu_p, bme_y, bme_p, bme_r, bme_a, bme_v, sg_1, sg_2, sg_3, sg_4, sg_5, sg_6, sg_7, sg_8, sg_9, sg_10, sg_11, sg_12, e, ts]

    def data_dict_set(self, rd)
        Description:
            updates the self.data with a dictionary. Differnet from setters
            because it does it updates the whole object not just individual
            attributes
        Parm:
            rd: updated data object.

    data_to_json()
        Desciption:
            Converts the dictionary to a Json format

    print_jsondata()
        Desciption:
            prints the current state of the json to the terminal

    all_rocketdata(self)
        Description:
            returns all data currently in self.data as an array

    convert_to_csv_string(self):
        Desciption:
            returns a single csv string that contains all the data in self.data

    """
    data = {}
    _lsm = Lsm()
    _bme = Bme()
    _encoders = Encoder()
    def __init__(self):
        self.data = {
            'bme': self._bme,
            'lsm': self._lsm,
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
                float
            ],
            'encoders': self._encoders,
            'time_stamp': float
        }

    # @property decorator makes the function below a getter
    @property
    def data(self):
        return self.data

    @property
    def lsm(self):
        return self.data['lsm']

    @lsm.setter
    def lsm(self, vals):
        if len(vals) == 10:
            ax, ay, az, mx, my, mz, gx, gy, gz, t = vals
            self.data['lsm']['acceleration_x'] = ax
            self.data['lsm']['acceleration_y'] = ay
            self.data['lsm']['acceleration_z'] = az
            self.data['lsm']['magnetometer_x'] = mx
            self.data['lsm']['magnetometer_y'] = my
            self.data['lsm']['magnetometer_z'] = mz
            self.data['lsm']['gyroscope_x'] = gx
            self.data['lsm']['gyroscope_y'] = gy
            self.data['lsm']['gyroscope_z'] = gz
            self.data['lsm']['temperature'] = t
        else: 
            print("LSM accepts 10 values in this order: Acceleration (x, y, z), magnetometer (x, y, z), gyroscope (x, y, z)")

    @lsm.setter
    def lsm_temp(self, t):
        self.data['lsm']['temperature'] = t

    @property
    def bme(self):
        return self.data['bme']

    @bme.setter
    def bme(self, vals):
        t, h, p = vals
        if len(vals) == 3:
            self.data['bme']['temperature'] = t
            self.data['bme']['humidity'] = h
            self.data['bme']['pressure'] = p
        else:
            print("BME accept exactly 3 values in this order: temperature, Humidity, Pressure")

    @bme.setter
    def bme_temp(self, t):
        self.data['bme']['temperature'] = t

    @property
    def strain_gauges(self):
        return self.data['strain_gauges']

    @strain_gauges.setter
    def strain_gauges(self, vals):
        if len(vals) == 12:
            self.data['strain_gauges'] = vals
        else:
            print("Strain gauges must be exactly 12 values")

    @property
    def encoders_position(self):
        return self.data['encoders']['position']

    @property
    def encoders_percent(self):
        return self.data['encoder']['percent']
    
    @encoders.setter
    def encoders(self, p):
        pos, perc = p
        self.data['encoders']['position'] = pos
        self.data['encoders']['percent'] = perc

    @property
    def time_stamp(self):
        return self.data['time_stamp']

    @time_stamp.setter
    def time_stamp(self, ts):
        self.data['time_stamp'] = ts

    #Set all sensor data
    @data.setter
    def setdata(self, vals):
        lsm_ax, lsm_ay, lsm_az, lsm_mx, lsm_my, lsm_mz, lsm_gx, lsm_gy, lsm_gz, lsm_t, bme_t, bme_h, bme_p, sg_1, sg_2, sg_3, sg_4, sg_5, sg_6, sg_7, sg_8, sg_9, sg_10, sg_11, sg_12, e, ts = vals
        print(lsm_t)
        self.imu([lsm_ax, lsm_ay, lsm_az, lsm_mx, lsm_my, lsm_mz, lsm_gx, lsm_gy, lsm_gz, lsm_t])
        self.bme([bme_t, bme_h, bme_p])
        self.strain_gauges([sg_1, sg_2, sg_3, sg_4, sg_5, sg_6, sg_7, sg_8, sg_9, sg_10, sg_11, sg_12])
        self.encoders(e)
        self.time_stamp(ts)

    def data_dict_set(self, rd):
        self.data.update(rd)

    def data_to_json(self):
        rocketData = json.dumps(self.data, indent = 4)
        print(rocketData)
        return rocketData

    def print_jsondata(self):
        jsonData = self.data_to_json(self.data)
        print(jsonData)

    def all_rocketdata(self):
        alldata = [
            self.data['lsm']['acceleration_x'],
            self.data['lsm']['acceleration_y'],
            self.data['lsm']['acceleration_z'],
            self.data['lsm']['magnetometer_x'],
            self.data['lsm']['magnetometer_y'],
            self.data['lsm']['magnetometer_z'],
            self.data['lsm']['gyroscope_x'],
            self.data['lsm']['gyroscope_y'],
            self.data['lsm']['gyroscope_z'],
            self.data['lsm']['temperature'],
            self.data['bme']['temperature'],
            self.data['bme']['humidity'],
            self.data['bme']['pressure'],
            self.data['strain_gauges'][0],
            self.data['strain_gauges'][1],
            self.data['strain_gauges'][2],
            self.data['strain_gauges'][3],
            self.data['strain_gauges'][4],
            self.data['strain_gauges'][5],
            self.data['strain_gauges'][6],
            self.data['strain_gauges'][7],
            self.data['strain_gauges'][8],
            self.data['strain_gauges'][9],
            self.data['strain_gauges'][10],
            self.data['strain_gauges'][11],
            self.data['encoders']['position'],
            self.data['time_stamp']
        ]
        return alldata

    def convert_to_csv_string(self):
        data_to_convert = self.all_rocketdata()
        csv_string = str(data_to_convert[0])
        for data in data_to_convert[1:]:
            csv_string += "," + str(data)

        return csv_string
