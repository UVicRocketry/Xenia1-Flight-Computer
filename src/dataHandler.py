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
	self.prev_height_change = 0
    	# previous change of height to compensate for Null case
    
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
    SPECIFIC_HEAT_DRYAIR = 1003.5

    #initialized altitude at launch pad
    INITIALIZED_ALTITUDE = 274.1
    # just an estimate, actual data will be collected on site

    #lapse rate of the air
    LAPSE_RATE = 0.0098
    # this is the standard dry air lapse rate, altered by initializeLapseRate()


    def initialize_lapse_rate(moist, pressure, temperature):
        """
        Takes moistness, pressure, and temperature readings at launch site to find lapse rate. 
        This should not be run after the initialization phase

        Paramaters:
            moist: float, water vapour pressure
            pressure: float, pressure reading
            temperature: float, temperature reading

        Returns:
            lapse_rate: float, lapse rate (... duh)
        """
        numerator_numerator = H2O_VAPOUR_HEAT * moist
        numerator_denomenator = temperature * SPECIFIC_GAS_H2O * (pressure - moist)

        numerator = GRAVITY * (1 + (numerator_numerator/numerator_denomenator))

        denomenator_numerator = H2O_VAPOUR_HEAT**2 * SPECIFIC_GAS_DRY * moist
        denomenator_denomenator = (SPECIFIC_GAS_H2O * temperature)**2 * (pressure - moist)

        denomenator = SPECIFIC_HEAT_DRYAIR + (denomenator_numerator/denomenator_denomenator)
        
        lapse_rate = (numerator/denomenator)
        
        return lapse_rate





    def altitude_barometric(pressure, init_pressure, init_temperature): # or altBaro, if needed
        """
        Takes pressure reading, initial pressure reading, and initial temperature reading to get altitude

        Parameters:
            pressure: float, current pressure reading
            init_pressure: float, initialized pressure reading, should not change after initialization
            init_temperature: float, initialized temperature reading, should not change after initialization

        Returns:
            alt_baro: float, altitude from barometric pressure
        """

        if type(pressure) != None:
            exponent = (-1 * GAS_CONSTANT * LAPSE_RATE) / (GRAVITY * ATMOSPHERIC_MOLAR_MASS)
            pressure_component = (pressure / init_pressure)**exponent

            alt_baro = (pressure_component * init_temperature / LAPSE_RATE) + INITIALIZED_ALTITUDE - init_temp

        elif type(pressure) == None:
            alt_baro = None

        return alt_baro
	



    def altitude_temperature_v1(curr_temperature, prev_temperature, prev_alt): # or altTemp if needed
        """
        Takes current temperature measurement, previous temperature measurement, 
        previous height, and previous height change to get altitude from temperature.

        Parameters:
            curr_temperature: float, current temperature reading
            prev_temperature: float, previous temperature reading
            prev_alt: float, previous height reading 
                      (note: could either be previous height reading from this function or a previous accepted height reading)

        Returns:
            alt_temperature: float, altitude from temperature
        """

        if type(curr_temperature) != None and type(prev_temperature) != None and curr_temperature < prev_temperature:
            dT = curr_temperature - prev_temperature
            dh = -1 * (dT/LAPSE_RATE)

            self.prev_height_change = dh

            alt_temperature = prev_alt + dh
            #prev_alt = alt_temperature

        elif (type(curr_temperature) == None or type(prev_temperature) == None) and curr_temperature < prev_temperature:
            dh = self.prev_height_change

            alt_temperature = prev_alt + dh
            prev_alt = alt_temperature

        elif curr_temperature > prev_temperature:
            alt_temperature = None

            prev_alt = prev_alt + self.prev_height_change


        return alt_temperature




    def altitude_temperature_v2(curr_temperature, init_temperature): # or altTemp if needed
        """
        Takes current temperature measurement and initialized temperature measurement change to get altitude from temperature.
        This version essentially turns the flight path into two linear directions (possibly ignore this, docstrings to be changed)

        Parameters:
            curr_temperature: float, current temperature reading
            init_temperature: float, initialized temperature, should not be altered after initialization phase

        Returns:
            alt_temeraturep: float, altitude from temperature
        """

        alt_temperature = -1 * ((curr_temperature - init_temperature)/LAPSE_RATE)

        return alt_temperature
    
    


    def get_velocity(current_alt, prev_alt, current_timestamp, prev_timestamp):
	"""
	
	"""
	
	if current_alt != type(None) and prev_alt != type(None):
		dh = current_alt - prev_alt
		dt = current_timestamp - prev_timestamp
		
		velocity = dh/dt
		
	else:
		velocity = None
		
	return velocity
