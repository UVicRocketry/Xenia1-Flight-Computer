import time
TIMEOUT = 5

class SafeValue:
    """Store a value from a sensor safely.
    __last_value is for black box __last_safe_value is for calculations
    
    ...

    Attributes
    ----------
    __last_value : float 
        The last read value

    __last_safe_value : float 
        The last non-null value for calculations
    
    __last_safe_time : float 
        CPU timestamp to get delta t

    __safe_range: float
        range of values that are acceptable

    Methods
    -------
    __in_safe_range() : Boolean 
        determines if a number is in __safe_range

    update() : N/A
        Receives a value updates __last_value with latest unsafe 
        value (None type possible). If value is not None,
        __last_safe_value is updated
    
    get_last_safe_value() : float
        Get the last safe value, or the backup if over time. If the last safe 
        value is older than TIMEOUT then this function will return the backup 
        Function. This is always called after  update() so if the sensor comes 
        back online, __last_safe_time and __last_safe_value will both be updated 
        and the  __backup_function will no longer be used.

    get_last_unsafe_value() : float 
        returns last unsafe value
    
    """

    def __init__(self, safe_range, backup_function):
        self.__last_value = backup_function()
        self.__last_safe_value = backup_function()
        self.__last_safe_time = time.time()
        self.__safe_range = safe_range
        # Proc to backup to
        # TODO: Backup value needs some thought because different values 
        #       and different types, and different needs. Some are crucial, some are not.
        self.__backup_function = backup_function
    

    def __in_safe_range(self, value):
        return (self.__safe_range[0] < value) and (value < self.__safe_range[1])


    def update(self, value):
        # Store the last read value blindly in __last_value
        self.__last_value = value

        # If the value is in range and not None, store it safely
        if (value is not None) and (self.__in_safe_range(value)):
            self.__last_safe_value = value
            self.__last_safe_time = time.time()

    
    def get_last_safe_value(self):
        if (self.__last_safe_time + TIMEOUT) > time.time():
            return self.__last_safe_value
        else:
            # TODO: What if no backup function.
            if self.__backup_function() is None:
                return None
            else:
                return self.__backup_function()

    def get_last_unsafe_value(self):
        return self.__last_value
