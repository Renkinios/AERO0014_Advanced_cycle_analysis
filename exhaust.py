import numpy as np
from findCp import *
from basic import *
# Assuming adiabatic expansion and no pressure losses, the total pressure and temperature values
# remain de same as the previous station so p9 = p0


def mach_number_nozzle(gamma, Stagna_pres_exhaust, pressure_exast) :
    return np.sqrt(2 / (gamma - 1) *((Stagna_pres_exhaust/pressure_exast)**((gamma - 1)/gamma) - 1))

def compute_mach_exhaust(Stagna_pres_exhaust, pressure_exast, gamma_begin, Stagna_temp_Exaust, m_fuel, m_air, R) :
    old_gamma = 0
    gamma     = gamma_begin
    tol       = 1e4
    iter      = 0
    iter_max  = 100
    f         = m_fuel/m_air

    while iter < iter_max and np.abs((old_gamma-gamma)/gamma) < tol :
        old_gamma   = gamma
        mach_number = mach_number_nozzle(gamma, Stagna_pres_exhaust, pressure_exast)
        temp_exaust = Stagna_temp_Exaust/(1 + mach_number * (( gamma - 1 )/2))
        Cp          = findCp((temp_exaust + Stagna_temp_Exaust) / 2 , f)
        gamma       = findGamma_indec(Cp, R)
        iter       += 1
    speed_sound =  np.sqrt(gamma * R * temp_exaust)
    V_10        = mach_number * speed_sound
    return V_10

def compute_thrust(V_10, m_air, m_fuel, v_0, mach_number) :
    if mach_number > 1 :
        return (m_air + m_fuel) * V_10 - m_air * v_0
    else :
        KeyError("The mach number is not supersonic")
    
def compute_specific_fuel_consumption(m_fuel, Trust) :
    return m_fuel / Trust





