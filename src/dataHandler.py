from rocketData import RocketData as rd
import csv
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
    def __init__(self, rd):
        self.rocket_data = rd
    
    # TODO: parm rd is a dict of updated 
    def update_rocket_data(self, rocketData):
        self.rocket_data = rd.data_dict_set(rocketData)
        
    def send_all_data(self, sendingTo, destination):
        if sendingTo == 'blackbox':
            data = self.rocket_data.convert_to_csv()
            f = open(destination, 'a')
            writer = csv.writer(f)
            writer.writerow(data)
            f.close()

    #gravitational acceleration 
    gravity = 9.80665

    #gas constant
    gas_const = 8.3144598

    #earth atmospheric molar mass
    atmo_molar_mass = 0.289644

    #vapourization heat of water
    H2O_vapour_heat = 2501000

    #specific gas constant of dry air
    specif_gas_const_dry = 287
    
    #specific gas constant of water vapour
    specif_gas_const_H2O = 461.5
    
    #specific heat of dry air
    specif_heat_dryair = 1003.5

    #initialized altitude at launch pad
    initialized_altitude = 274.1
    # just an estimate, actual data will be collected on site

    #previous calculated height change
    prev_height_change = 0
    # previous change of height to compensate for Null case

    #lapse rate of the air
    lapse_rate = 0.0098
    # this is the standard dry air lapse rate, altered by initializeLapseRate()


    def initializeLapseRate(moist, press, temp):
        """
        Takes moistness, pressure, and temperature readings at launch site to find lapse rate. 
        This should not be run after the initialization phase

        Paramaters:
            moist: float, water vapour pressure
            press: float, pressure reading
            temp: float, temperature reading

        Returns:
            lapse_rate: float, lapse rate (... duh)
        """
        numerator_numerator = H2O_vapour_heat * moist
        numerator_denomenator = temp * specif_gas_const_H2O * (press - moist)

        numerator = gravity * (1 + (numerator_numerator/numerator_denomenator))

        denomenator_numerator = H2O_vapour_heat**2 * specif_gas_const_dry * moist
        denomenator_denomenator = (specif_gas_const_H2O * temp)**2 * (press - moist)

        denomenator = specif_heat_dryair + (denomenator_numerator/denomenator_denomenator)
        
        lapse_rate = (numerator/denomenator)
        
        return lapse_rate





    def altitudeBarometric(press, init_press, init_temp): # or altBaro, if needed
        """
        Takes pressure reading, initial pressure reading, and initial temperature reading to get altitude

        Parameters:
            press: float, current pressure reading
            init_press: float, initialized pressure reading, should not change after initialization
            init_temp: float, initialized temperature reading, should not change after initialization

        Returns:
            alt_baro: float, altitude from barometric pressure
        """

        if type(press) != None:
            exponent = (-1 * gas_const * lapse_rate) / (gravity * atmo_molar_mass)
            pressure_component = (press / init_press)**exponent

            alt_baro = (pressure_component * init_temp / lapse_rate) + initialized_altitude - init_temp

        elif type(press) == None:
            alt_baro = None

        return alt_baro
	



    def altitudeTemperature_v1(curr_temp, prev_temp, prev_alt): # or altTemp if needed
        """
        Takes current temperature measurement, previous temperature measurement, 
        previous height, and previous height change to get altitude from temperature.

        Parameters:
            curr_temp: float, current temperature reading
            prev_temp: float, previous temperature reading
            prev_alt: float, previous height reading 
                      (note: could either be previous height reading from this function or a previous accepted height reading)

        Returns:
            alt_temp: float, altitude from temperature
        """

        # NOTE: need a previous height global variable alongside the prev_dh to prevent compounding errors,
        # 			or a way to have the altitude reading be inputted as such

        global prev_height_change

        if type(curr_temp) != None and type(prev_temp) != None and curr_temp < prev_temp:
            dT = curr_temp - prev_temp
            dh = -1 * (dT/lapse_rate)

            prev_height_change = dh

            alt_temp = prev_alt + dh
            prev_h = alt_temp

        elif (type(curr_temp) == None or type(prev_temp) == None) and curr_temp < prev_temp:
            dh = prev_height_change

            alt_temp = prev_alt + dh
            prev_alt = alt_temp

        elif T_c > T_p:
            alt_temp = None

            prev_alt = prev_alt + prev_height_change


        return alt_temp




    def altitudeTemperature_v2(curr_temp, init_temp): # or altTemp if needed
        """
        Takes current temperature measurement and initialized temperature measurement change to get altitude from temperature.
        This version essentially turns the flight path into two linear directions (possibly ignore this, docstrings to be changed)

        Parameters:
            curr_temp: float, current temperature reading
            init_temp: float, initialized temperature, should not be altered after initialization phase

        Returns:
            alt_temp: float, altitude from temperature
        """

        alt_temp = -1 * ((curr_temp - init_temp)/lapse_rate)

        return alt_temp
    
    
    
    
