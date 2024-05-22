def convacc(value, input_unit, output_unit):
    """
    Convert acceleration between different units.
    
    Parameters:
    value (float): The value to be converted.
    input_unit (str): The unit of the input value.
    output_unit (str): The unit to convert to.
    
    Returns:
    float: The converted value.
    """
    units_to_meters_per_second_squared = {
        'ft/s^2': 0.3048,
        'm/s^2': 1,
        'km/s^2': 1000,
        'in/s^2': 0.0254,
        'km/h-s': 0.277778,
        'mph/s': 0.44704,
        'G': 9.80665
    }
    
    value_in_meters_per_second_squared = value * units_to_meters_per_second_squared[input_unit]
    converted_value = value_in_meters_per_second_squared / units_to_meters_per_second_squared[output_unit]
    
    return converted_value

def convang(value, input_unit, output_unit):
    """
    Convert angles between different units.
    
    Parameters:
    value (float): The value to be converted.
    input_unit (str): The unit of the input value.
    output_unit (str): The unit to convert to.
    
    Returns:
    float: The converted value.
    """
    units_to_degrees = {
        'deg': 1,
        'rad': 57.2958  # 1 radian = 57.2958 degrees
    }
    
    value_in_degrees = value * units_to_degrees[input_unit]
    converted_value = value_in_degrees / units_to_degrees[output_unit]
    
    return converted_value

def convangacc(value, input_unit, output_unit):
    """
    Convert angular acceleration between different units.
    
    Parameters:
    value (float): The value to be converted.
    input_unit (str): The unit of the input value.
    output_unit (str): The unit to convert to.
    
    Returns:
    float: The converted value.
    """
    units_to_degrees_per_second_squared = {
        'deg/s^2': 1,
        'rad/s^2': 57.2958,  # 1 radian/s^2 = 57.2958 degrees/s^2
        'rpm/s^2': 360  # 1 rpm/s^2 = 360 degrees/s^2
    }
    
    value_in_degrees_per_second_squared = value * units_to_degrees_per_second_squared[input_unit]
    converted_value = value_in_degrees_per_second_squared / units_to_degrees_per_second_squared[output_unit]
    
    return converted_value

def convangvel(value, input_unit, output_unit):
    """
    Convert angular velocity between different units.
    
    Parameters:
    value (float): The value to be converted.
    input_unit (str): The unit of the input value.
    output_unit (str): The unit to convert to.
    
    Returns:
    float: The converted value.
    """
    units_to_degrees_per_second = {
        'deg/s': 1,
        'rad/s': 57.2958,  # 1 radian/s = 57.2958 degrees/s
        'rpm': 6  # 1 rpm = 6 degrees/s
    }
    
    value_in_degrees_per_second = value * units_to_degrees_per_second[input_unit]
    converted_value = value_in_degrees_per_second / units_to_degrees_per_second[output_unit]
    
    return converted_value

def convdensity(value, input_unit, output_unit):
    """
    Convert density between different units.
    
    Parameters:
    value (float): The value to be converted.
    input_unit (str): The unit of the input value.
    output_unit (str): The unit to convert to.
    
    Returns:
    float: The converted value.
    """
    units_to_kg_per_cubic_meter = {
        'lbm/ft^3': 16.0185,
        'kg/m^3': 1,
        'slug/ft^3': 515.378,
        'lbm/in^3': 27679.9
    }
    
    value_in_kg_per_cubic_meter = value * units_to_kg_per_cubic_meter[input_unit]
    converted_value = value_in_kg_per_cubic_meter / units_to_kg_per_cubic_meter[output_unit]
    
    return converted_value

def convforce(value, input_unit, output_unit):
    """
    Convert force between different units.
    
    Parameters:
    value (float): The value to be converted.
    input_unit (str): The unit of the input value.
    output_unit (str): The unit to convert to.
    
    Returns:
    float: The converted value.
    """
    units = {
        'lbf': 1,
        'N': 0.224809
    }
    return value * units[output_unit] / units[input_unit]

def convmass(value, input_unit, output_unit):
    """
    Convert mass between different units.
    
    Parameters:
    value (float): The value to be converted.
    input_unit (str): The unit of the input value.
    output_unit (str): The unit to convert to.
    
    Returns:
    float: The converted value.
    """
    units = {
        'lbm': 1,
        'kg': 2.20462,
        'slug': 0.0685218
    }
    return value * units[output_unit] / units[input_unit]

def convpres(value, input_unit, output_unit):
    """
    Convert pressure between different units.
    
    Parameters:
    value (float): The value to be converted.
    input_unit (str): The unit of the input value.
    output_unit (str): The unit to convert to.
    
    Returns:
    float: The converted value.
    """
    units = {
        'psi': 1,
        'Pa': 0.000145038,
        'psf': 0.00694444,
        'atm': 14.6959
    }
    return value * units[output_unit] / units[input_unit]

def convlength(value, input_unit, output_unit):
    """
    Convert length between different units.
    
    Parameters:
    value (float): The value to be converted.
    input_unit (str): The unit of the input value.
    output_unit (str): The unit to convert to.
    
    Returns:
    float: The converted value.
    """
    units_to_meters = {
        'ft': 0.3048,
        'm': 1,
        'km': 1000,
        'in': 0.0254,
        'mi': 1609.34,
        'naut mi': 1852
    }
    
    # Convert the input value to meters
    value_in_meters = value * units_to_meters[input_unit]
    
    # Convert the value in meters to the output unit
    converted_value = value_in_meters / units_to_meters[output_unit]
    
    return converted_value

def convtemp(value, input_unit, output_unit):
    """
    Convert temperature between different units.
    
    Parameters:
    value (float): The value to be converted.
    input_unit (str): The unit of the input value.
    output_unit (str): The unit to convert to.
    
    Returns:
    float: The converted value.
    """
    if input_unit == 'K':
        if output_unit == 'C':
            return value - 273.15
        elif output_unit == 'F':
            return value * 9/5 - 459.67
        elif output_unit == 'R':
            return value * 9/5
    elif input_unit == 'C':
        if output_unit == 'K':
            return value + 273.15
        elif output_unit == 'F':
            return value * 9/5 + 32
        elif output_unit == 'R':
            return (value + 273.15) * 9/5
    elif input_unit == 'F':
        if output_unit == 'K':
            return (value + 459.67) * 5/9
        elif output_unit == 'C':
            return (value - 32) * 5/9
        elif output_unit == 'R':
            return value + 459.67
    elif input_unit == 'R':
        if output_unit == 'K':
            return value * 5/9
        elif output_unit == 'C':
            return (value - 491.67) * 5/9
        elif output_unit == 'F':
            return value - 459.67

def convspeed(value, input_unit, output_unit):
    """
    Convert velocity between different units.
    
    Parameters:
    value (float): The value to be converted.
    input_unit (str): The unit of the input value.
    output_unit (str): The unit to convert to.
    
    Returns:
    float: The converted value.
    """
    units_to_meters_per_second = {
        'ft/s': 0.3048,
        'm/s': 1,
        'km/s': 1000,
        'in/s': 0.0254,
        'km/h': 0.277778,
        'mph': 0.44704,
        'kts': 0.514444,
        'ft/min': 0.00508
    }
    
    # Convert the input value to meters per second
    value_in_meters_per_second = value * units_to_meters_per_second[input_unit]
    
    # Convert the value in meters per second to the output unit
    converted_value = value_in_meters_per_second / units_to_meters_per_second[output_unit]
    
    return converted_value


