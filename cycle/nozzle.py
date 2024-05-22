# Need to know if the nozzle is shock or not if not speration by something
import numpy as np
from findCp import *
from basic import *

def compute_nozzle_converging_pressure_ratio_phi_n(gamma_start, TiT_tot, m_air, m_fuel, R) : 
    """
    Calculate the nozzle pressure ratio.
    
    Parameters:
    gamma (float): The adiabatic index.
    
    Returns:
    float: The nozzle pressure ratio approximatly between 1.83 -1.89.
    """
    gamma_old = 0
    gamma = gamma_start
    tol = 1e4
    iter = 0
    iter_max = 100
    M = 1           # to look if we have some shock 
    f = m_fuel/m_air
    while iter < iter_max and np.abs((gamma_old - gamma)) / gamma < tol :
        gamma_old = gamma
        Ti     = Total_temp2static_temp(gamma, TiT_tot, M) 
        CP = findCp((Ti + TiT_tot)/2, f)
        gamma = findGamma_indec(CP, R)
        iter += 1
    return gamma, Ti

def compute_nozzle_converging_pressure_ratio_prime(gamma, total_p, static_pressure_start_cycle) :
    '''
    Usually gamma  of ejection gases is between 1.3 and 1.4. This means that π∗
    n should be between 1.83 and 1.89. If the
    calculated pressure ratio is in between these two values is necessary to recalculate the NPR in order to determined if
    the nozzle is choked or not. But if is above 1.9, we are sure it is choked.
    '''
    phi_n = (1 + (gamma - 1) / 2)**(gamma / (gamma - 1))
    rap_p = total_p/static_pressure_start_cycle
    if rap_p>= phi_n : 
        print("############ Danger ############")
        print("The nozzle is shock")
        print("##################################")

        shock = 1 
    else : 
        print("############ Danger #############")
        print("The nozzle don't subize a shock")
        print("##################################")

        shock = 0
    return shock

def compute_nozzle_converging_area(gamma, R, static_T5,total_p, dot_m) :

    speed = mac_number2speed(gamma, R, static_T5, 1)
    static_pressure = Total_pression2static_pression(gamma, total_p, 1)
    rho = static_pressure/ (R * static_T5)
    return (dot_m / (rho * speed)), static_pressure, speed





