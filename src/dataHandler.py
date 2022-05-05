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
        Desciption:
            only called in send_all
        Parm:
            sendingTo can either be "blackbox", "antenna"
            
    send_imu(self, sendingTo)
        Desciption:
            only called in send_all
        Parm:
            sendingTo can either be "blackbox", "antenna"
            
    send_strain_gauges(self, sendingTo)
         Desciption:
            only called in send_all
        Parm:
            sendingTo can either be "blackbox", "antenna"
            
    send_all_data(self, sendingTo)
        Desciption:
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
        rocket_data = rd
    
    # TODO: parm rd is a dict of updated 
    def update_rocket_data(self, rocketData):
        rocket_data = rd.data_dict_set(rocketData)
        
    def send_bme(self, sendingTo):
        # call format data
        return

    def send_imu(self, sendingTo):
        return

    def send_strain_gauges(self, sendingTo):
        return
    
    def send_all_data(self, sendingTo, destination):
        if sendingTo == 'blackbox':
            data = self.convert_to_csv()
            f = open(destination, 'a')
            writer = csv.writer(f)
            writer.writerow(data)
            f.close()
        
       
    def format_to_send(self, sendingTo, dataToFomat):
        return

    

