from ISA import *
import numpy as np
from basic import *

def compute_massFlow_correct2massFlow(total_temp, total_press, m_dot_sea_lvl) :
    ISA_sea = ISA_condition(0)
    return (m_dot_sea_lvl * total_press/ISA_sea.P0)/(np.sqrt(total_temp/ISA_sea.T0))

def compute_RPM_corrected2RPM(RPM_sea_vl, Total_temp) :
    ISA_sea = ISA_condition(0)
    return RPM_sea_vl * np.sqrt(Total_temp/ISA_sea.T0)

def compute_power_corrected2power(power_sea, Total_temp, Total_press) :
    ISA_sea = ISA_condition(0)
    return power_sea * np.sqrt(Total_temp/ISA_sea.T0) * (Total_press/ISA_sea.P0) 

def compute_rho_corrected2rho(P_stat, T_stat, M_mac, gamma, rho_sea) :
    ISA_sea = ISA_condition(0)
    P = Static_temp2Total_Temp(gamma, P_stat, M_mac)
    T = Static_temp2Total_Temp(gamma, T_stat, M_mac)
    return (ISA_sea.P0/P) * (ISA_sea.T0/T_stat) * rho_sea



def compute_sound_speed_corrected2sounnd_speed(T_stat, M_mac, gamma, speed_sound_sea) :
    ISA_sea = ISA_condition(0)
    T = Static_temp2Total_Temp(gamma, T_stat, M_mac)
    return np.sqrt(T/ISA_sea.T0) *speed_sound_sea

