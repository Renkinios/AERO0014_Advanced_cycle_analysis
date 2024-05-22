import numpy as np
from findCp import *

def Total_pressure_combustion(comb_chamber_pressur_loss,initial_pressure) : 
    '''
    Returns the total pressure at the exit of the combustion chamber
    Inputs :
    - comb_chamber_pressur_loss : Pressure loss in the combustion chamber
    - initial_pressure : Initial pressure
    Outputs :
    - Total_pressure : Total pressure at the exit of the combustion chamber
    '''
    return initial_pressure * (1 - comb_chamber_pressur_loss )


def mass_flow_chamber(mass_flow,TiT,ToT,Ref_temp,Comb_eff,FuelLowerHeat,Starf) : 
    '''
    Return mass_flow of the fuel
    Inputs :
    - mass_flow :  mass flow of the air [kg/s]
    - TiT       :  Temperature in input of the chamber
    - ToT       :  Temperature in output of the chamber
    - Ref_temp  :  Temperature of reference for Cp -> 288.15 K
    - Comb_eff  :  Combustion chamber efficiency
    - FuelLowerHeat : Fuel lower heating value ∆hf
    - Starf     : Starting value for f

    '''
    f        = Starf
    f_old    = 1
    tol      = 1e4
    iter     = 0
    iter_max = 100
    while  iter < iter_max and np.abs(f_old - f)/f < tol :
        f_old = f 
        CP4   = findCp((Ref_temp + TiT)/2, 0)
        CP5   = findCp((Ref_temp + ToT)/2,f)
        mdotf = mass_flow * (CP4 * (TiT - Ref_temp) - CP5 * (ToT - Ref_temp))/(CP5 *(ToT - Ref_temp) - Comb_eff * FuelLowerHeat)
        f     = mdotf/mass_flow
        iter += 1

    return mdotf 

def compute_temperature_afterburn_Wet(m_air ,m_fuel, m_after_burn, TiT, T_ref, start_cp, eff_af, heating_value) :
    """
    Compute temperature afterburn, considering new fuel the fuel afterburn going to have a worst efficiency but mroe trust
    Args :
        - m_air : mass flow air
        - m_fuel : mass flow fuel
        - m_after_burn : mass flow afterburn added in wet mode
        - TiT : temp in the antrance
        - T_ref : temp of reference ft hp 
        - start_cp : first guess
        - eff_af   : effiiency of the afterburn 
        - heating_value : chaleur added to the afterbunr the delta_h increasing 

    """

    Cp_output     = start_cp
    Cp_output_old = 0
    Cp_input      = findCp((TiT + T_ref)/2, m_fuel/m_air) # before add fuel 
    tol           = 1e4
    iter          = 0 
    iter_max      = 100

    while iter < iter_max and np.abs((Cp_output_old - Cp_output)/Cp_output) < tol : 
        Cp_output_old = Cp_output
        Total_temp    = ((m_air + m_fuel)*Cp_input * (TiT - T_ref) + eff_af * heating_value * m_after_burn)/((m_air + m_fuel + m_after_burn) * Cp_output)
        Cp_output     = findCp((Total_temp + T_ref)/2, (m_fuel + m_after_burn)/ m_air)
        iter         += 1

    return Total_temp

