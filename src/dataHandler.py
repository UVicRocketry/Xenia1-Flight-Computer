from rocketData import RocketData as rd
import csv

#gravitational acceleration 
GRAVITY = 9.80665

#gas constant
GAS_CONSTANT = 8.3144598

#earth atmospheric molar mass
ATMOSPHERIC_MOLAR_MASS = 0.289644

#vapourization heat of water
H2O_VAPOUR_HEAT = 2501000

#specific gas constant of dry air
SPECIFIC_GAS_DRY = 287

#specific gas constant of water vapour
SPECIFIC_GAS_H2O = 461.5

#specific heat of dry air
SPECIFIC_HEAT_DRY_AIR = 1003.5

#initialized altitude at launch pad
INITIALIZED_ALTITUDE = 274.1
# just an estimate, actual data will be collected on site

#lapse rate of the air
LAPSE_RATE = 0.0098

class SendData:
    """
    This only deals with sending the rocketdata. RocketData class in src/rocketData.py deals with manipulating the data.  
    
    ...

    Attributes
    ----------
    rocket_data 
        protected attribute that holds all the sensor rocket data imported from rocketData

    Methods
    -------
    send_bme(self, sendingTo)
        Description:
            only called in send_all
        Parm:
            sendingTo can either be "blackbox", "antenna"
            
    send_imu(self, sendingTo)
        Description:
            only called in send_all
        Parm:
            sendingTo can either be "blackbox", "antenna"
            
    send_strain_gauges(self, sendingTo)
         Description:
            only called in send_all
        Parm:
            sendingTo can either be "blackbox", "antenna"
            
    send_all_data(self, sendingTo)
        Description:
            For sending to blackbox: Calls convert_to_csv to get a list of all the data and saves it to a csv 
        Parm:
            sendingTo can either be "blackbox", "antenna"
            destination: the name of the csv file to save to
            
    format_to_send(self, sendingTo)
        Description:
            formats the data into a sendable state
        Parm:
            sendingTo: can either be "blackbox", "ground"
            dataToFomat: Which sensor is needed to be called
    -------
    """

    # this is the standard dry air lapse rate, altered by initializeLapseRate()
    def __init__(self, rd):
        self.rocket_data = rd
        self.prev_height_change = 0
        # previous change of height to compensate for Null case




