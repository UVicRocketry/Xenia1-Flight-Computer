# gonna use this for defining all variables in the header file
# im using the assumption that the None value will work to provide a value-less variable

# Also, any comment after a bit of code that looks identical is the placeholder I had beforehand
# The _equivalent is just there to show that it needed an equivalent to the subject


PD_SCK: """byte_equivalent""" = None
# Power down and Serial Clock Input Pin

COUNT: """byte_equivalent""" = None
# Number of channels to read

DOUT: """byte_equivalent""" = None # theres an * in front of this in c++, investigate
# Serial Data Output Pin

GAIN: """byte_equivalent""" = None
# Amplification factor

debugEnabled: bool = None

OFFSETS: """long_equivalent""" = None
# Offset value determined by the tare() function

SCALE: float = None

TIMEOUT: """long_equivalent""" = 300



# HX711MULTI::HX711MULTI

# Im assuming byte type in c++ are floats since they hold the same bit value

def hx711Multi(count: int, dout: """byte_equivalent""", pd_sck: """byte_equivalent""", gain: """byte_equivalent"""):
    """
    Defines the clock and data pin, channel, and gain factor
    Channel selection is made by passing the appropriate gain, being 128 or 64 for channel A, and 32 for channel B
    COUNT is the number of channels
    DOUT is an array of pin numbers, legnth "count", one entry per channel
    
    From what I can tell, this is the initialization function for the chip (or something similar)
    """
    PD_SCK = pd_sck
    DOUT = dout
    COUNT = count
    
    debugEnabled = False
    
    pinMode(PD_SCK, OUTPUT) # pinMode_equivalent(PD_SCK, OUTPUT)
    
    for i in range(count):
        pinMode(DOUT[i], INPUT) # pinMode_equivalent(DOUT[i], INPUT)
        
    setGain(gain)




# HX711MULTI::is_ready

def isReady():
    """
    Checks if the HX711 is ready
    
    
    From data sheet:
    
    When output data is not ready for retrieval:
    - Digital output pin (DOUT) is high
    - Serial clock input (PD_SCK) should be low. 
    When DOUT goes to low:
    - Indicates that data is ready for retrieval
    """
    result = True
    
    for bit in range(COUNT): # changed i to bit, might not be a good idea
        if (digitalRead(DOUT[i]) == HIGH): # digitalRead_equivalent(DOUT[i]) == HIGH
            result = False
            
    return result




# HX711MULTI::set_gain

def setGain(gain: """byte_equivalent"""):
    """
    Sets the gain factor
    This function will only take effect after a read() call
    
    Channel A can be set for 128 or 64 gain, channel B has a fixed gain of 32
    
    Depending on the parameter, the channel will be set to either A or B
    """
    match gain:
        case 128:
            GAIN = 1
            break
        
        case 64:
            GAIN = 3
            break
        
        case 32:
            GAIN = 2
            break
        
    digitalWrite(PD_SCK, LOW) #v digitalWrite_equivalent(PD_SCK, LOW)
    
    # read()_equivalent if there is one




# HX711MULTI::get_count

def getCount():
    """
    Returns the number of channels
    """
    return COUNT




# HX711MULTI::tare

def tare(times: """byte_equivalent""", tolerance: """some other stuff"""):
    """
    Sets the OFFSET value for tare weight
    Returns True if the offsets have been reset for the scale during this call
    
    times: how many times to read the tare value
    tolerance: the maximum deviation of samples, above which tare attempts will be rejected (if set to 0, ignored)
    """
    # currently unable to define values[COUNT], minValues[COUNT], and maxValues[COUNT]
    # this is because I dont know what it means. Check Aila or dad 
    
    
    for i in range(COUNT):
        
        # determine how to use the 0x7FFFFFFF etc in python
    
    for i in range(times):
        readRaw(values)
        
        for j in range(COUNT):
            
            if values[j] < minValues[j]:
                minValues[j] = values[j]
                
            if values[j] > maxValues[j]:
                maxValues[j] = values[j]
            
        
    if tolerance != 0 and times > 1:
        
        for i in range(COUNTS):
            if abs(maxValues[i] - minValues[i] > tolerance):
                
                if debugEnabled:
                    # these are all the outputs of an equivalent serial print
                    # ("Rejecting tare: (")
                    # (i)
                    # (") ")
                    # this one is serial.println
                    # (abs(maxValues[i] - minValues[i]))
                    
                return False
    
    for i in range(COUNT):
        OFFSETS[i] = values[i]
        
    return True




# HX711MULTI::read

def read(result: """long equivalent"""): # determine where you get result from
    """
    Waits for the chip to be ready and returns a reading
    Essentially an offset option for readRaw()
    """
    readRaw(result)
    
    if result != None:
        for j in range(COUNT):
            result[j] -= OFFSETS[j]




# HX711MULTI::readRaw

def readRaw(result: """long equivalent"""):
    """
    Waits for the chip to be ready and returns a reading
    Does not offset values
    
    Note: TIMEOUT == 300, its set in the header file
    """
    startTime = millis() # millis()_equivalent
    
    
    
    while is_ready() == False:
        
        if (millis() - startTime) > TIMEOUT: # millis()_equivalent
            
            # Serial.print("Error\n") find equivalent
            forceRead()
            delay(5) # delay_equivalent(5)
            break
            
    
    
    if isReady():
        
        for i in range(24):
            
            digitalWrite(PD_SCK, HIGH) # digitalWrite_equivalent(PD_SCK, HIGH)
            delayMicroseconds(1)       # delayMicroseconds_equivalent(1)
            
            if result != None:
                for j in range(COUNT):
                    # bitWrite_equivalent(result[j], 23 - i, digitalRead_equivalent(DOUT[j]))
                    
            digitalWrite(PD_SCK, LOW)  # digitalWrite_equivalent(PD_SCK, LOW)
            delayMicroseconds(1)       # delayMicrosecond_equivalent(1)
            
            
        for i in range(GAIN):
            digitalWrite(PD_SCK, HIGH) # digitalWrite_equivalent(PD_SCK, HIGH)
            digitalWrite(PD_SCK, LOW)  # digitalWrite_equivalent(PD_SCK, LOW)
            
        
        if result != None:
            
            for j in range(COUNT):
                
                # this stuff is currently beyond me. Investigate further
            
            
# A lot of things in here that I dont know how to translate just yet




# HX711MULTI::setDebugEnable

def setDebugEnable(debugEnable: bool):
    """
    Sets whether or not debugging is turned on
    """
    debugEnabled = debugEnable




# HX711MULTI::power_down

def powerDown():
    """
    Puts the chip into power down mode
    """
    digitalWrite(PD_SCK, LOW)  # digitalWrite_equivalent(PD_SCK, LOW)
    digitalWrite(PD_SCK, HIGH) # digitalWrite_equivalent(PD_SCK, HIGH)




# HX711MULTI::power_up

def powerUp():
    """
    Wakes the chip up
    """
    digitalWrite(PD_SCK, LOW) # digitalWrite_equivalent(PD_SCK, LOW)




# HX711MULTI::setTimeOut

def setTimeOut(timeout: int):
    """
    Changes the TIMEOUT value, initially defined as 300 during definitions
    """
    TIMEOUT = timeout




# HX711MULTI::forceRead

def forceRead():
    """
    
    """
    data: """long_equivalent""" = None
    
    for i in range(24):
        digitalWrite(PD_SCK, HIGH) # digitalWrite_equivalent(PD_SCK, HIGH)
        
        for j in range(COUNT):
            # bitWrite_equivalent(data, 23-i, digitalRead_equivalent(DOUT[j]))
        
        digitalWrite(PD_SCK, LOW)  # digitalWrite_equivalent(PD_SCK, LOW)
    
    for i in range(GAIN):
        digitalWrite(PD_SCK, HIGH) # digitalWrite_equivalent(PD_SCK, HIGH)
        digitalWrite(PD_SCK, LOW)  # digitalWrite_equivalent(PD_SCK, LOW)

