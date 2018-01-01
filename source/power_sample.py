# power_sample.py 
# PowerGrid - Group 6
# CMPT 318 D2 Cyber Security
# Summer 2017

import datetime


def enforce_type(instance, type_list):
    types = []
    # Check if type is correct
    for type_ in type_list:
        if isinstance(instance, type_):
            return
        types.append(str(type_))
    
    # Type is not correct
    error_message = "Object is of type " + str(type(instance)) \
            + " but must be of type " + ' or '.join(types)
    raise TypeError(error_message)
        
        
# Try conversion from type(_object) to any. None can be specified
# in _conversion_tuple_list to to attempt conversion on any type
def convert_type(instance, conversion_tuple_list=[]):
    if not conversion_tuple_list:
        # No conversions specified
        return instance
        
    # Attempt conversions in list order
    for conversion_tuple in conversion_tuple_list:
        if (conversion_tuple[0] is None or
                isinstance(instance, conversion_tuple[0])):
            try:
                return conversion_tuple[1](instance)
            except:
                pass
            
    # No successful conversions
    raise TypeError("convert_type cannot convert")


# Check types and correct. Returns corrected type, or raises
# error if no specified conversion is possible
def correct_type(instance, type_list, conversion_tuple_list=[]):
    try:
        enforce_type(instance, type_list)
    except TypeError as error:
        try:
            instance = convert_type(instance, conversion_tuple_list)
            enforce_type(instance, type_list) # Confirm conversion
        except TypeError:
            raise error
    return instance

class PowerSample:
    
    def __init__(self, date, time, global_active_power, 
            global_reactive_power, voltage, global_intensity, 
            sub_metering_1, sub_metering_2, sub_metering_3):
        self.date = date
        self.time = time
        self.global_active_power = global_active_power
        self.global_reactive_power = global_reactive_power
        self.voltage = voltage
        self.global_intensity = global_intensity
        self.sub_metering_1 = sub_metering_1
        self.sub_metering_2 = sub_metering_2
        self.sub_metering_3 = sub_metering_3
        
    def __str__(self):
        return str(self.properties)
            
            
## Getters and setters
    
    @property
    def date(self):
        return self._date
    @date.setter
    def date(self, date):
        self._date = correct_type(
                date,
                [datetime.date],
                [(datetime.datetime,
                datetime.datetime.date)])
        
    @property
    def time(self):
        return self._time
    @time.setter
    def time(self, time):
        self._time = correct_type(
                time,
                [datetime.time],
                [(datetime.datetime,
                datetime.datetime.time)])
        
    @property
    def global_active_power(self):
        return self._global_active_power
    @global_active_power.setter
    def global_active_power(self, global_active_power):
        self._global_active_power = correct_type(
                global_active_power,
                [float, type(None)],
                [(None, lambda x: float(x))])
        
    @property
    def global_reactive_power(self):
        return self._global_reactive_power
    @global_reactive_power.setter
    def global_reactive_power(self, global_reactive_power):
        self._global_reactive_power = correct_type(
                global_reactive_power,
                [float, type(None)],
                [(None, lambda x: float(x))])
        
    @property
    def voltage(self):
        return self._voltage
    @voltage.setter
    def voltage(self, voltage):
        self._voltage = correct_type(
                voltage,
                [float, type(None)],
                [(None, lambda x: float(x))])
        
    @property
    def global_intensity(self):
        return self._global_intensity
    @global_intensity.setter
    def global_intensity(self, global_intensity):
        self._global_intensity = correct_type(
                global_intensity,
                [float, type(None)],
                [(None, lambda x: float(x))])
        
    @property
    def sub_metering_1(self):
        return self._sub_metering_1
    @sub_metering_1.setter
    def sub_metering_1(self, sub_metering_1):
        self._sub_metering_1 = correct_type(
                sub_metering_1,
                [float, type(None)],
                [(None, lambda x: float(x))])
        
    @property
    def sub_metering_2(self):
        return self._sub_metering_2
    @sub_metering_2.setter
    def sub_metering_2(self, sub_metering_2):
        self._sub_metering_2 = correct_type(
                sub_metering_2,
                [float, type(None)],
                [(None, lambda x: float(x))])
        
    @property
    def sub_metering_3(self):
        return self._sub_metering_3
    @sub_metering_3.setter
    def sub_metering_3(self, sub_metering_3):
        self._sub_metering_3 = correct_type(
                sub_metering_3,
                [float, type(None)],
                [(None, lambda x: float(x))])
            
    @property
    def properties(self):
        return self._properties
    @properties.getter
    def properties(self):
        return {
                'date':self.date,
                'time':self.time,
                'global_active_power':self.global_active_power,
                'global_reactive_power':self.global_reactive_power,
                'voltage':self.voltage,
                'global_intensity':self.global_intensity,
                'sub_metering_1':self.sub_metering_1,
                'sub_metering_2':self.sub_metering_2,
                'sub_metering_3':self.sub_metering_3
                }    
    @properties.setter
    def properties(self, properties):
        self.date = properties['date']
        self.time = properties['time']
        self.global_active_power = properties['global_active_power']
        self.global_reactive_power = properties['global_reactive_power']
        self.voltage = properties['voltage']
        self.global_intensity = properties['global_intensity']
        self.sub_metering_1 = properties['sub_metering_1']
        self.sub_metering_2 = properties['sub_metering_2']
        self.sub_metering_3 = properties['sub_metering_3']
    
    
    
    
    
    
    
    
    
    
