# TODO: Make into usable python in X1-AV-42. 
TIMEOUT = 0.5

# TODO: This is basically pseudo code. Would probably explode before the rocket
class SafeValue:
    """Store a value from a sensor safely.
    
    This is only for values used in calculations. For values that
    are only used in logging, just try else null."""

    def __init__(self, safe_range, backup_function, read_function):
        # The last read value
        self.__last_value
        # The last non-nil value
        self.__last_safe_value
        # CPU timestamp to get delta t
        self.__last_safe_time
        self.__safe_range = safe_range
        # Proc to backup to
        # TODO: Backup value needs some thought because different values 
        #       and different types, and different needs. Some are crucial, some are not.
        
        # These should be closures, procs, function pointers, or similar
        # Don't know what these are in Python -MC
        self.__backup_function
        self.__read_function

    def update(self, value):
        # Store the last read value blindly
        self.__last_value = value

        # If the value is in range and not nil, store it safely
        if value and (value in self.__safe_range):
            self.__last_safe_value = value
            self.__last_safe_time = Time.now()

    # TODO: Bad name.
    def valid_and_safe_value():
        """Get the last safe value, or the backup if over time"""
        if valid_time_since:
            __last_safe
        else:
            # TODO: What if no backup function.
            self.__backup_function(time_since_fail, last_safe)
