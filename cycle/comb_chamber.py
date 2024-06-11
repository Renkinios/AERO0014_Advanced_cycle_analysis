import numpy as np
from findCp import *
from basic import *

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
    f_old    = 0
    tol      = 1e-4
    iter     = 0
    iter_max = 100
    CP4   = findCp((Ref_temp + TiT)/2, 0)
    while  iter < iter_max and   tol < np.abs(f_old - f)/f  :
        f_old = f 
        CP5   = findCp((Ref_temp + ToT)/2,f)
        mdotf = mass_flow * (CP4 * (TiT - Ref_temp) - CP5 * (ToT - Ref_temp))/(CP5 *(ToT - Ref_temp) - Comb_eff * FuelLowerHeat)
        f     = mdotf/mass_flow
        iter += 1

    return mdotf 

def compute_f_generall(CP_cc, T4, T3, eff_cc, entalpis):
    """
    Come form one exercice where we need to determined the mass flow he give to use the CP_cc
    """
    return CP_cc *(T4 - T3)/(eff_cc * entalpis)

def compute_temperature_before_chamber(m_air ,m_fuel, ToT, T_ref, start_cp, heating_value, eff_combustion) : 
    """
    start_cp : 1000
    """
    Cp_output     = start_cp
    Cp_output_old = 0
    Cp_input      = findCp((ToT + T_ref)/2, (m_fuel)/ m_air) # before add fuel 
    print("Cp_input", Cp_input)
    tol           = 1e-4
    iter          = 0 
    iter_max      = 100

    while iter < iter_max and tol < np.abs((Cp_output_old - Cp_output)/Cp_output)  : 
        Cp_output_old = Cp_output
        Total_temp    = T_ref + ((m_fuel + m_air) * Cp_input * (ToT - T_ref) - m_fuel * eff_combustion * heating_value)/(m_air * Cp_output)
        Cp_output     = findCp((Total_temp + T_ref)/2, 0)
        iter         += 1
    return Total_temp, Cp_output


############################ Afterburn #####################################""
def mass_flow_chamber_afterburn(mass_flow,m_fuel,TiT,ToT,Ref_temp,Comb_eff,FuelLowerHeat) : 
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
    f_old    = 0
    tol      = 1e-4
    iter     = 0
    iter_max = 100
    f_without_afternburn = m_fuel/mass_flow
    CP4      = findCp((Ref_temp + TiT)/2, f_without_afternburn)
    f        = f_without_afternburn
    while  iter < iter_max and tol < np.abs(f_old - f)/f  :
        f_old = f 
        CP5   = findCp((Ref_temp + ToT)/2,f)
        mdotf_after_burn = (mass_flow + m_fuel) * (CP4 * (TiT - Ref_temp) - CP5 * (ToT - Ref_temp))/(CP5 *(ToT - Ref_temp) - Comb_eff * FuelLowerHeat)
        f     = (mdotf_after_burn + m_fuel)/mass_flow
        iter += 1

    return mdotf_after_burn 

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
    tol           = 1e-4
    iter          = 0 
    iter_max      = 100

    while iter < iter_max and tol < np.abs((Cp_output_old - Cp_output)/Cp_output)  : 
        Cp_output_old = Cp_output
        Total_temp    = T_ref + ((m_air + m_fuel) * Cp_input * (TiT - T_ref) + eff_af * heating_value * m_after_burn)/((m_air + m_fuel + m_after_burn) * Cp_output)
        Cp_output     = findCp((Total_temp + T_ref)/2, (m_fuel + m_after_burn)/ m_air)
        iter         += 1

    if iter > iter_max : 
        print("Danger didn't converge")
    return Total_temp

def compute_temperature_after_chamber(m_air ,m_fuel, TiT, T_ref, start_cp, eff_af, heating_value) :
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
    Cp_input      = findCp((TiT + T_ref)/2, 0) # before add fuel 
    tol           = 1e-4
    iter          = 0 
    iter_max      = 100

    while iter < iter_max and tol < np.abs((Cp_output_old - Cp_output)/Cp_output)  : 
        Cp_output_old = Cp_output
        Total_temp    = T_ref + ((m_air )*Cp_input * (TiT - T_ref) + eff_af * heating_value * m_fuel)/((m_air + m_fuel ) * Cp_output)
        Cp_output     = findCp((Total_temp + T_ref)/2, (m_fuel )/ m_air)
        iter         += 1
    return Total_temp


def compute_F(gamma, M) : 
    """
    This is the fonction to converte the all m_dot_tot to m_dot_stat 
    """
    return np.sqrt(gamma) * M * (1 + (gamma - 1)/2 * M**2)**(-(gamma + 1)/(2 * (gamma - 1)))
def compute_fuse_cond_shock_iter(p_tot, T_tot, gamma, Ae, At) : 

    iter = 0
    iter_max = 100
    Mac_start = 4
    start_F = compute_F(gamma,Mac_start)
    F_0 = compute_F(gamma, 1)
    tol = 1e-5
    for i in (1,5, 10, 50, 100, 200 ,300 ,200,300, 400, 500, 600, 7000, 800, 900, 1000,) : 
        while iter < iter_max and  np.abs(F_0 - start_F *Ae/At) > tol  :
            # print(F_0 - start_F *Ae/At, Mac_start + iter * 1/i)
            MAC_end = Mac_start + iter * 1/i
            start_F = compute_F(gamma, MAC_end)
            if F_0 - start_F *Ae/At > 0 :
                start_F = Mac_start + iter * 0.001
                break
            iter +=1
        
    print("Start_f_end", np.abs(F_0 - start_F *Ae/At))
    print("diff_gama", F_0 - compute_F(gamma,5.2) * Ae/At )
    return MAC_end



