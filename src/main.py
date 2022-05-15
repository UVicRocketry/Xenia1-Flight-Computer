# loop that just keeps going (as long as the computer is engaged)
# run this script once were good to go
# A lot of try catch baby

from gpioReader import GPIOReader
import sys

#TODO: 
# - Implement initialize() for any setup
# - Implement main loop for mid flight controls
# - Implement error handling to avoid systems failure mid flight


def initialize():
    
    return 0 


if __name__ == "__main__":
    
    ### Main code goes here###
    test_mode = False #use "python main.py test" to initialize test mode

    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_mode = True

    
    running = True 
      
    if(test_mode): 
        while(running):
            #retrieves random data from GPIOReader
            gpio = GPIOReader(test_mode, False, False, False, False, False, False, False)
            gpio.retrieveData()
            
            ## Update rocketData object
            
            ## Do airbrakes stuff
            
            ## Send rocketData to datahandler call send function

    else:
        
        while(running):
        ## Setup a loop that continues until we tell it to stop
            ## Read GPIO Input
            print("")
            ## Update rocketData object
            
            ## Send GPIO rocketData to datahandler for output

            ## Do air brakes math (to be implemented later with kris)

    exit(0)
