# Need to know if the nozzle is shock or not if not speration by something
import numpy as np
from findCp import *
from basic import *
from cycle.exhaust import *


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
    tol = 1e-4
    iter = 0
    iter_max = 100
    M = 1           # to look if we have some shock 
    f = m_fuel/m_air
    while iter < iter_max and tol < np.abs((gamma_old - gamma)) / gamma  :
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
        print("Rap_p", rap_p)
        print("phi_n", phi_n)
        print("The nozzle is shock")
        print("##################################")

        shock = 1 
    else : 
        print("############ Danger #############")
        print("The nozzle don't subize a shock")
        print("##################################")

        shock = 0
    return shock

def compute_nozzle_converging_area_mach(gamma, R, static_T5,total_p, dot_m, mac_number) :
    """
    This fonction is for a mach number of one i cna chan
    """

    speed = mac_number2speed(gamma, R, static_T5, mac_number)
    static_pressure = Total_pression2static_pression(gamma, total_p, mac_number)
    rho = static_pressure/ (R * static_T5)
    return (dot_m / (rho * speed)), static_pressure, speed

def compute_nozzle_area(speed, static_pres, static_temps, R, dot_m) : 
    rho = static_pres/ (R * static_temps)
    return dot_m / (rho * speed)


def trust_nozzle_all(gamma_start, total_temp, total_pression, flux_air, flux_fuel, v_0, isa) :

    # first step see if we have a mach number : 
    # this is calculate with a mac of 1 to sea if we have a shock or not
    gamma, static_temp = compute_nozzle_converging_pressure_ratio_phi_n(gamma_start, total_temp, flux_air, flux_fuel, isa.R)
    shock = compute_nozzle_converging_pressure_ratio_prime(gamma, total_pression, isa.P0)

    if shock == 1 :
        # the mac didn't change so M = 1
        area, static_pressure, V_out = compute_nozzle_converging_area_mach(gamma, isa.R, static_temp, total_pression, flux_air + flux_fuel, 1)
        print("area", area)
        print("static_pressure", static_pressure)
        print("Speed output", V_out)
        Trust = compute_thrust(V_out, flux_air, flux_fuel, v_0, static_pressure, isa.P0, area, shock)
    else :
        # The mac change so need to calculate it iteratively
        V_out, gamma, Cp, mach_number = compute_mach_exhaust(total_pression, isa.P0, gamma_start, total_temp, flux_fuel, flux_air, isa.R)
        area, _, _ = compute_nozzle_converging_area_mach(gamma, isa.R, isa.P0, total_pression, flux_air + flux_fuel, mach_number)
        # Normally don't need compute area
        Trust = compute_thrust(V_out, flux_air, flux_fuel, v_0, isa.P0, isa.P0, area, shock)
    return Trust, V_out


