import time
#time.time() returns the time from a specific date in seconds. I think the date is sometime in 1970. This is used to determine timeout.

# TODO: Make into usable python in X1-AV-42. 
#TIMEOUT is the amount of time in seconds until the last non None value be valid. After that the backup function will be used.
TIMEOUT = 5

# TODO: This is basically pseudo code. Would probably explode before the rocket
class SafeValue:
    """Store a value from a sensor safely.
    __last_value is for black box __last_safe_value is for calculations"""

    def __init__(self, safe_range, backup_function):
        # The last read value
        self.__last_value
        # The last non-nil value for calculations
        self.__last_safe_value
        # CPU timestamp to get delta t
        self.__last_safe_time
        #range of values that are acceptable
        self.__safe_range = safe_range
        # Proc to backup to
        # TODO: Backup value needs some thought because different values 
        #       and different types, and different needs. Some are crucial, some are not.
        
        # These should be closures, procs, function pointers, or similar
        # Don't know what these are in Python -MC
        self.__backup_function = backup_function
    
    def __in_safe_range(self, value):
        """determines if a number is in __safe_range"""
        return (self.__safe_range[0] < value) and (value < self.__safe_range[1])

    def update(self, value):
        """recieves a value updates __last_value with latest unsafe value (None type possible). If value is not None,
        __last_safe_value is updated"""
        # Store the last read value blindly in __last_value
        self.__last_value = value

        # If the value is in range and not None, store it safely
        if (value is not None) and (self.__in_safe_range(value)):
            self.__last_safe_value = value
            self.__last_safe_time = time.time()

    
    def get_last_safe_value(self):
        """Get the last safe value, or the backup if over time. If the last safe value is older than TIMEOUT then this function
        will return the backup Function. This is always called after update() so if the sensor comes back online, __last_safe_time
        and __last_safe_value will both be updated and the __backup_function will no longer be used"""
        if (self.__last_safe_time + TIMEOUT) > time.time():
            return self.__last_safe_value
        else:
            # TODO: What if no backup function.
            if self.__backup_function is None:
                return None
            else:
                return self.__backup_function()

    def get_last_unsafe_value(self):
        """returns last unsafe value"""
        return self.__last_value
