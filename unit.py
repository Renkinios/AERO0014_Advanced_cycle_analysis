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
        'rad': 57.2958,  # 1 radian = 57.2958 degrees
        'grad': 0.9     # 1 grad = 0.9 degrees
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
        'rpm/s^2': 360 / 60  # 1 rpm/s^2 = 6 degrees/s^2 (1 rpm = 6 degrees)
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
    units_to_newton = {
        'lbf': 4.44822,  # 1 lbf = 4.44822 N
        'N': 1          # 1 N = 1 N
    }
    
    value_in_newton = value * units_to_newton[input_unit]
    converted_value = value_in_newton / units_to_newton[output_unit]
    
    return converted_value


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
    units_to_kg = {
        'lbm': 0.453592,  # 1 lbm = 0.453592 kg
        'kg': 1,          # 1 kg = 1 kg
        'slug': 14.5939   # 1 slug = 14.5939 kg
    }
    
    value_in_kg = value * units_to_kg[input_unit]
    converted_value = value_in_kg / units_to_kg[output_unit]
    
    return converted_value

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
    units_to_pascal = {
        'psi': 6894.76,    # 1 psi = 6894.76 Pa
        'Pa': 1,           # 1 Pa = 1 Pa
        'psf': 47.8803,    # 1 psf = 47.8803 Pa
        'atm': 101325,     # 1 atm = 101325 Pa
        'bar': 100000,     # 1 bar = 100000 Pa

    }
    
    value_in_pascal = value * units_to_pascal[input_unit]
    converted_value = value_in_pascal / units_to_pascal[output_unit]
    
    return converted_value



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

    return value  # If the input_unit and output_unit are the same, return the value as is.


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


def convenergy(value, input_unit, output_unit):
    """
    Convert energy between different units.
    
    Parameters:
    value (float): The value to be converted.
    input_unit (str): The unit of the input value.
    output_unit (str): The unit to convert to.
    
    Returns:
    float: The converted value.
    """
    units_to_joules = {
        'J': 1,             # 1 joule = 1 joule
        'calorie': 4.184,       # 1 calorie = 4.184 joules
        'kilocalorie': 4184,    # 1 kilocalorie = 4184 joules
        'kWh': 3600000,         # 1 kWh = 3600000 joules
        'BTU': 1055.06,         # 1 BTU = 1055.06 joules
        'erg': 1e-7,            # 1 erg = 1e-7 joules
        'foot-pound': 1.35582   # 1 foot-pound = 1.35582 joules
    }
    
    value_in_joules = value * units_to_joules[input_unit]
    converted_value = value_in_joules / units_to_joules[output_unit]
    
    return converted_value
