import numpy as np
from findCp import *
from basic import *
# Assuming adiabatic expansion and no pressure losses, the total pressure and temperature values
# remain de same as the previous station so p9 = p0


def mach_number_nozzle(gamma, Total_pressure, static_pressure) :
    return np.sqrt(2 / (gamma - 1) *((Total_pressure/static_pressure)**((gamma - 1)/gamma) - 1))


def compute_mach_exhaust(Total_pressure, static_pressure, gamma_begin, Total_temp, m_fuel, m_air, R) :
    """
    Calculate the exhaust speed by the mach number.
    Args:
        Total_pressure (float): The stagnation pressure of the exhaust.
        static_pressure (float): The pressure of the exhaust.
        gamma_begin (float): The adiabatic index.
        Total_temp (float): The stagnation temperature of the exhaust.
        m_fuel (float): The mass flow rate of the fuel.
        m_air (float): The mass flow rate of the air.
        R (float): The gas constant.
    """
    old_gamma = 0
    gamma     = gamma_begin
    tol       = 1e4
    iter      = 0
    iter_max  = 200
    f         = m_fuel/m_air

    while iter < iter_max and np.abs((old_gamma-gamma)/gamma) < tol :
        old_gamma   = gamma
        mach_number = mach_number_nozzle(gamma, Total_pressure, static_pressure)
        static_temp = Total_temp2static_temp(gamma, Total_temp, mach_number)
        Cp          = findCp((static_temp + Total_temp) / 2, f)
        gamma       = findGamma_indec(Cp, R)
        iter       += 1

    print("gamma \t", gamma)
    print("Temp \t", static_temp)
    speed_sound =  np.sqrt(gamma * R * static_temp)
    V_10        = mach_number * speed_sound
    print("The mach number is : \t", mach_number)
    print("speed sound is : \t", speed_sound)
    return V_10

def compute_thrust(V_10, m_air, m_fuel, v_0, p_ex, p_0, A_ex, shock_converging) :
    if shock_converging == 1 :
        return (m_air + m_fuel) * V_10 - m_air * v_0 + (p_ex -p_0) * A_ex
    else :
        return (m_air + m_fuel) * V_10 - m_air * v_0 


def compute_specific_fuel_consumption(m_fuel, Trust) :
    return (m_fuel / Trust) *10 * 3600 # kg/ daN / h

def Compute_exaust_velocity_trust(T, m_air, m_fuel, v_initial) : 
    return (T + m_air * v_initial) /(m_air + m_fuel)





