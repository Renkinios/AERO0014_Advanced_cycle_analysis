# High pressure rubine (HPT)
import numpy as np
from findCp import *
from basic import *


def power_produce_turbine(PowerComp, meca_eff_shaft) : 
    """
    Power produce by the turbine
    Args:
        PowerComp (float)     : Power produce by the compressor
        meca_eff_shaft (float): Mechanical efficiency of the shafts
    Returns:
        PowerTurbine (float)  : Power produce by the turbine
    """
    return PowerComp / meca_eff_shaft

def compute_temp_turbine(TiT,P_hpt,m_a,m_f,ToT_beging) :
    """
    Retuurn temperature after the turbine 
    Args :
    TiT : Temperature initial
    P_hpt : Power de la turbine
    m_a   : mass flow of the air
    m_f   : mass flow of the fuel 
    ToT_beging : Temperature begining fluide
    """
    ToT_old  = 0 
    ToT      = ToT_beging
    tol      = 1e-4
    iter     = 0
    iter_max = 100
    f        = m_f/m_a
    while iter < iter_max and tol < np.abs((ToT_old - ToT)) /ToT  :
        Cp_5_6 = findCp((TiT + ToT)/2,f)
        ToT    = (-P_hpt/ ((m_a+m_f) * Cp_5_6)) + TiT
        iter  += 1
    return ToT,Cp_5_6

# def pressure_turbine(TiT, Tot, eta_isentropic, C_p, R, P_i_T) : 
#     gamma = findGamma_indec(C_p, R)
#     rapport_press = ratio_pressure_isentropique(TiT, Tot, eta_isentropic,gamma)
#     return  1/rapport_press * P_i_T 
def pressure_turbine(TiT, ToT, eta_isentropic, C_p, R, P_i_T) : 
    gamma = findGamma_indec(C_p, R)
    ToT_s = comp_temp_isenropic(ToT, TiT, eta_isentropic)
    rapport_pres = (ToT_s/TiT)**(gamma/(gamma-1))
    return  rapport_pres * P_i_T 


def compute_eff_iso_turbine(TiT, ToT, pit, pot, gamma) : 
    return (1 - ToT/TiT)/(1 - (pit/pot)**(-(gamma - 1)/gamma))

def eff_poly2eff_iso_turbine(gamma, eff_poly, pi_t) :
    return (1 - pi_t **(-eff_poly * (gamma -1)/gamma)) / (1 - pi_t **(-(gamma -1)/gamma))

def eff_iso2eff_poly_turbine(gamma, eff_iso_turbine, pi_t):
    return -gamma / ((gamma - 1) * np.log(pi_t)) * np.log(1 - eff_iso_turbine + eff_iso_turbine * pi_t ** (-(gamma - 1) / gamma))

def comp_work_turbine(cp, tit, ratio_p, eff_s, gamma) : 
    """
    ratio p : definis comme p1/p2 
    """
    return eff_s * tit * (ratio_p**((gamma - 1)/gamma) - 1)

def compute_work_turbine_entalpis(Cp, TiT, ToT) : 
    return Cp * (TiT - ToT)


def compute_temp__turbine_with_poly(T1, ratio_pressure, eff_pol, gamma) :
    """
    formule vient page 56  T2/T1 = (P2/P1)**(eff_pol *(gamma -1)/gamma)
    """
    return (ratio_pressure)**(eff_pol *(gamma -1)/gamma) * T1

