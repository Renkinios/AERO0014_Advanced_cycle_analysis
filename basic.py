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

def computIsoSEff(T0_1, T0_2, Pi, gamma) :
    """
    Calculate the isentropic efficiency.
    
    Parameters:
    T0_1 (float): The temperature at station 1.
    T0_2 (float): The temperature at station 2.
    Pi (float): The pressure ratio.
    gamma (float): The adiabatic index.
    
    Returns:
    float: The isentropic efficiency.
    """
    return (Pi**((gamma-1)/gamma) - 1) / (T0_2/T0_1 - 1)

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

def turbIsoSEff(pi_t, T0_1, T0_2, C_p, R) :
    """
    Calculate the turbine isentropic efficiency.
    
    Parameters:
    pi_t (float): The turbine pressure ratio.
    T0_1 (float): The temperature at station 1.
    T0_2 (float): The temperature at station 2.
    C_p (float): The specific heat at constant pressure.
    R (float): The gas constant.
    
    Returns:
    float: The turbine isentropic efficiency.
    """
    gamma = findGamma_indec(C_p, R)
    return  (1 - T0_2/T0_1) / (1 - pi_t**(-(gamma-1)/gamma))


def eff_poly2eff_iso(pressure_ratio,gamma, poly_eff) :
    """
    Calculate the isentropic efficieny with the polytrpîc efficiency.
    
    Parameters:
    pressure_ratio (float): The pressure ratio.
    gamma (float): The adiabatic index.
    isentropic_eff (float): The isentropic efficiency.
    
    Returns:
    float: The polytropic efficiency.
    """
    return (pressure_ratio**((gamma-1)/gamma) - 1) / (pressure_ratio**((gamma-1)/(gamma * poly_eff)) - 1)

def eff_iso2eff_poly(pressure_ratio, gamma, iso_eff):
    """
    Calculer l'efficacité polytropique à partir de l'efficacité isentropique.

    Paramètres:
    pressure_ratio (float): Le rapport de pression (\(\pi_{c,A}\)).
    gamma (float): L'indice adiabatique (\(\gamma_a\)).
    iso_eff (float): L'efficacité isentropique (\(\eta_{c,s,A}\)).

    Retourne:
    float: L'efficacité polytropique (\(\eta_p\)).
    """
    term1 = np.log(pressure_ratio ** ((gamma - 1) / gamma))
    term2 = np.log((pressure_ratio ** ((gamma - 1) / gamma) - 1) / iso_eff + 1)
    return term1 / term2


def ratio_pressure_isentropique(TiT,ToT,efficency_isentropic,gamma) : 
    ToT_s = comp_temp_isenropic(ToT, TiT, efficency_isentropic)
    
    return (1 - (1- ToT/TiT)/efficency_isentropic)**(-gamma/(gamma -1))

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
