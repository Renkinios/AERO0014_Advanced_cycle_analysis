import numpy as np
from findCp import *

def thermal_eff(W,Q_c):
    """
    Calculate the thermal efficiency.
    
    Parameters:
    W (float): The work.
    Q_c (float): The heat.
    
    Returns:
    float: The thermal efficiency.
    """
    return W/Q_c

def propu_eff(T,v_init,W) :
    """
    Calculate the propulsive efficiency.
    
    Parameters:
    T (float): The thrust.
    v_init (float): The initial velocity.
    W (float): The work.
    
    Returns:
    float: The propulsive efficiency.
    """
    return T*(v_init)/W


def compute_work_W(mass_flow_input, speed_input ,mass_flow_output, speed_output) : 
    """
    Calculate the work.
    
    Parameters:
    mass_flow_input (float): The mass flow rate of the input.
    speed_input (float): The speed of the input.
    mass_flow_output (float): The mass flow rate of the output.
    speed_output (float): The speed of the output.
    
    Returns:
    float: The work.
    """
    return (mass_flow_output * speed_output**2 - mass_flow_input * speed_input**2) / 2

def compute_heat_Q(mass_fuel_burn, hentalpi_burn) :
    """
    Calculate the heat.
    
    Parameters:
    mass_fuel_burn (float): The mass of the fuel burned.
    hentalpi_mass (float): The enthalpy mass.
    
    Returns:
    float: The heat.
    """
    return mass_fuel_burn * hentalpi_burn 

def comp_temp_isenropic(T0, Ti, eff_iso) :
    """
    Calculate the isentropic temperature.
    
    Parameters:
    T0 (float): The temperature.
    Ti (float): The initial temperature.
    eff_iso (float): The isentropic efficiency.
    
    Returns:
    float: The isentropic temperature.
    """
    return Ti  + (T0 - Ti) / eff_iso

def compute_iso_eff_pure(TiT, ToT, ToT_iso) :
    return (TiT - ToT) / (TiT - ToT_iso)

def compute_Temp_iso(pot, pit, TiT, gamma) : 
    
    return TiT * (pot/pit) **((gamma - 1)/gamma)

def comp_eff_propu_res(v_start, v_end) : 
    return 2 * v_start/(v_start + v_end)

def comp_eff_termique_res(heating_val, mass_air, mass_fuel, v_start, v_end) : 
    return mass_air * ( v_end**2 - v_start**2 ) / (2 * mass_fuel * heating_val)

 
def compute_mechanical_power_shock(m_fuel, exaust_speed, mdot, start_speed, p0, rho0, p_end, rho_end) : 
    return (mdot+m_fuel)*(exaust_speed**2 /2 + (p_end/rho_end)) - mdot*(start_speed**2 /2 + (p0/rho0))

