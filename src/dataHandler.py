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
        
    #gravity 
    g = 9.80665

    #gas_constant 
    R = 8.3144598

    #atmo_molar_mass 
    M = 0.289644

    #H2O_vapourize_heat 
    H_v = 2501000

    #spec_gas_const_dry 
    R_sd = 287
    
    #spec_gas_const_H2O 
    R_sw = 461.5
    
    #spec_heat_dry_air 
    c_pd = 1003.5

    #initialized_altitude
    h_i = 274.1
    # just an estimate, actual data will be collected on site

    prev_dh = 0
    # previous change of height to compensate for Null case


    def initializeLapseRate(e, p, T):
        """
        Takes moistness, pressure, and temperature readings at launch site to find lapse rate. 
        This should not be run after the initialization phase

        Paramaters:
            e: float, moistness
            p: float, pressure reading
            T: float, temperature reading

        Returns:
            lapse_rate: float, lapse rate (... duh)
        """
        numerator_numerator = H_v * e
        numerator_denomenator = T * R_sw * (p - e)

        numerator = g * (1 + (numerator_numerator/numerator_denomenator))

        denomenator_numerator = H_v**2 * R_sd * e
        denomenator_denomenator = (R_sw * T)**2 * (p - e)

        denomenator = c_pd + (denomenator_numerator/denomenator_denomenator)
        
        lapse_rate = (numerator/denomenator)
        
        return lapse_rate





    def altitudeBarometric(p, p_i, T_i): # or altBaro, if needed
        """
        Takes pressure reading, initial pressure reading, and initial temperature reading to get altitude

        Parameters:
            p: float, current pressure reading
            p_i: float, initialized pressure reading, should not change after initialization
            T_i: float, initialized temperature reading, should not change after initialization

        Returns:
            alt_B: float, altitude from barometric pressure
        """

        if type(p) != None:
            exponent = (-1 * R * L) / (g * M)
            pressure_component = (p / p_i)**exponent

            alt_B = (pressure_component * T_i / L) + h_i - T_i

        elif type(p) == None:
            alt_B = None

        return alt_B
	



    def altitudeTemperature_v1(T_c, T_p, prev_h): # or altTemp if needed
        """
        Takes current temperature measurement, previous temperature measurement, 
        previous height, and previous height change to get altitude from temperature.

        Parameters:
            T_c: float, current temperature reading
            T_p: float, previous temperature reading
            prev_h: float, previous height reading 
                            (note: could either be previous height reading from this function or a previous accepted height reading)

        Returns:
            alt_T: float, altitude from temperature
            prev_dh: new previous altitude change value
        """

        # NOTE: need a previous height global variable alongside the prev_dh to prevent compounding errors,
        # 			or a way to have the altitude reading be inputted as such

        global prev_dh

        if type(T_c) != None and type(T_p) != None and T_c < T_p:
            dT = T_c - T_p
            dh = -1 * (dT/L)

            prev_dh = dh

            alt_T = prev_h + dh
            prev_h = alt_T

        elif (type(T_c) == None or type(T_p) == None) and T_c < T_p:
            dh = prev_dh

            alt_T = prev_h + dh
            prev_h = alt_T

        elif T_c > T_p:
            alt_T = None

            prev_h = prev_h + prev_dh


        return alt_T




    def altitudeTemperature_v2(T, T_i): # or altTemp if needed
        """
        Takes current temperature measurement and initialized temperature measurement change to get altitude from temperature.
        This version essentially turns the flight path into two linear directions

        Parameters:
            T: float, current temperature reading
            T_i: float, initialized temperature, should not be altered after initialization phase

        Returns:
            alt_T: float, altitude from temperature
        """

        alt_T = -1 * ((T - T_i)/L)

        return alt_T
    
    
    
    
