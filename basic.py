import numpy as np
import math
from thermo import *
def compute_mac_number(gamma, R, T, speed) :
    """
    Calculate the Mach number.
    
    Parameters:
    gamma (float): Adiabetique index
    R (float): The gas constant.
    T (float): The temperature.
    
    Returns:
    float: The Mach number.
    """
    v_sound = np.sqrt(gamma * R * T)
    print("v_soud", v_sound)
    return speed / v_sound

def mac_number2speed(gamma, R, T, Mac_number) :
    """
    Calculate the speed.
    
    Parameters:
    gamma (float): Adiabetique index
    R (float): The gas constant.
    T (float): The temperature.
    Mac_number (float): The Mach number.
    
    Returns:
    float: The speed.
    """
    v_sound = np.sqrt(gamma * R * T)
    return Mac_number * v_sound

def findGamma_indec(C_p, R) : 
    """
    Calculate the adiabatic index.
    
    Parameters:
    C_p (float): The specific heat at constant pressure.
    R (float): The gas constant.
    
    Returns:
    float: The adiabatic index.
    """
    return C_p / (C_p - R)


def Total_temp2static_temp(gamma, total_temp, mac_number) :
    return (total_temp)/(1 + (gamma - 1) / 2 * mac_number**2)

def Static_temp2Total_Temp(gamma, basic_temp, mac_number) :
    T0 = basic_temp * (1 + (gamma - 1) / 2 * mac_number**2)
    return T0

def Total_pression2static_pression(gamma, total_pression, mac_number) :
    return  total_pression/(1 + (gamma - 1) / 2 * mac_number**2)**(gamma / (gamma - 1))

def static_pression2TotalPression(gamma, basic_pression, mac_number) :
    return basic_pression * (1 + (gamma - 1) / 2 * mac_number**2)**(gamma / (gamma - 1))


def atmosisa(altitude):
    """
    Calculate the temperature and pressure at a given altitude using the International Standard Atmosphere (ISA) model.
    
    Parameters:
    altitude (float): Altitude in meters
    
    Returns:
    tuple: Temperature in Kelvin, Pressure in Pascals
    """
    # Constants
    T0 = 288.15  # Sea level standard temperature in Kelvin
    P0 = 101325  # Sea level standard pressure in Pascals
    L = 0.0065  # Temperature lapse rate in K/m (for Troposphere)
    R = 287.05  # Specific gas constant for dry air in J/(kg·K)
    g0 = 9.80665  # Standard gravity in m/s^2

    if altitude < 0:
        raise ValueError("Altitude must be non-negative")

    if altitude <= 11000:  # Troposphere
        T = T0 - L * altitude
        P = P0 * (T / T0) ** (-g0 / (L * R))
    elif 11000 < altitude <= 20000:  # Lower Stratosphere
        T = 216.65  # Temperature is constant in this layer
        P = 22632.1 * math.exp(-g0 * (altitude - 11000) / (R * T))
    elif 20000 < altitude <= 32000:  # Mid Stratosphere
        T = 216.65 + 0.001 * (altitude - 20000)
        P = 5474.89 * (T / 216.65) ** (-g0 / (0.001 * R))
    elif 32000 < altitude <= 47000:  # Upper Stratosphere
        T = 228.65 + 0.0028 * (altitude - 32000)
        P = 868.02 * (T / 228.65) ** (-g0 / (0.0028 * R))
    elif 47000 < altitude <= 51000:  # Lower Mesosphere
        T = 270.65  # Temperature is constant in this layer
        P = 110.91 * math.exp(-g0 * (altitude - 47000) / (R * T))
    elif 51000 < altitude <= 71000:  # Mid Mesosphere
        T = 270.65 - 0.0028 * (altitude - 51000)
        P = 66.94 * (T / 270.65) ** (-g0 / (-0.0028 * R))
    elif 71000 < altitude <= 84852:  # Upper Mesosphere
        T = 214.65 - 0.002 * (altitude - 71000)
        P = 3.96 * (T / 214.65) ** (-g0 / (-0.002 * R))
    else:
        raise ValueError("Altitude out of range (0-84852 meters)")

    return T, P
