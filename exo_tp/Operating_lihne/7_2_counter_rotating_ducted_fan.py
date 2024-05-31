
import sys
import os

# Chemin absolu du répertoire où se trouve ce script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Chemin du répertoire contenant les fichiers à importer
# parent_dir = os.path.join(current_dir, '..', '..', 'cycle')
direct_dir = os.path.join(current_dir, '..', '..')

# sys.path.append(parent_dir)
sys.path.append(direct_dir)

from unit import *
from ISA import *
from cycle.ambiante_condition import *
from cycle.comb_chamber import *
from cycle.Intake import *
from cycle.compressor import *
from cycle.turbine import *
from cycle.exhaust import *
from thermo import *
from cycle.nozzle import *
from fonction_print import *
from corrected_cond import *
from interpolation import *

import numpy as np


alpha = 20 # bypass ratio 

p_r = 101325 
Tr = 288

M = 0.85
altitude = 10000

ISA = ISA_condition(altitude,True)
ISA.T0 = 268.34
ISA.P0 = 69681.7



T2, P2 = ambiante_condition(ISA.gamma_index, M, ISA.T0, ISA.P0)
print_stat(P2, T2, "Ambiante")

D_t = 0.8
D_h = 0.55
Nozzle_ara = np.pi *(D_t**2 - D_h**2)/4

m_dot_co = np.array([74.04, 75.55, 78.27, 79.59, 81.10, 81.86])
ratio_p_fan = np.array([1.3054, 1.3040, 1.2932, 1.2837, 1.2672, 1.2552])
eff_f  = np.array([0.9016, 0.91377, 0.92997, 0.93454, 0.93422, 0.92911])

ratio_p_fan_interpolation = cubic_splane_interpol(m_dot_co, ratio_p_fan)
eff_f_interpolation = cubic_splane_interpol(m_dot_co, eff_f)

# condition tout suceed m_s = m_n
# like  we have the area we can find the flux massique --> A * rho * speed = m_s

iter = 0
iter_max = 50
tol = 1e-4
m_dot_co = np.linspace(np.min(m_dot_co), np.max(m_dot_co), 1000)

delta_dot = 2
def iter_7_2(iter) :
    m_s = alpha/(1 + alpha) * compute_massFlow_correct2massFlow(T2, P2, m_dot_co[iter])
    gamma2, Cp2, T3 = compute_tot_isentropic_directly_eff_compressor(eff_f_interpolation(m_dot_co[iter]), 1.38, ratio_p_fan_interpolation(m_dot_co[iter]), T2, ISA.R)
    P3 = P2 * ratio_p_fan_interpolation(m_dot_co[iter])
    speed, gamma, Cp, mach_number, static_temp = compute_mach_exhaust(P3, ISA.P0, gamma2, T3, 0, m_s, ISA.R)
    rho = ISA.P0 / (ISA.R * static_temp)
    m_noze = Nozzle_ara * rho * speed
    delta_dot = (m_s - m_noze)
    return delta_dot, m_s, m_noze


arg_min = 0 
arg_max = len(m_dot_co) - 1

while iter < iter_max and delta_dot > tol :
    arg_mid =(arg_min + arg_max) //2

    delta_dot_min,m_s_min,m_noze_min = iter_7_2(arg_min)
    delta_dot_max,m_s_max,m_noze_max = iter_7_2(arg_max)
    delta_dot_mid, m_s, m_noze = iter_7_2(arg_mid)
    print("######################" , iter, "######################")
    print(f"m_dot_cor_min :{m_dot_co[arg_min]:.2f}, delta_dot_min : {delta_dot_min:.2f}, m_noze : {m_s_min:.2f}, delta_dot_mid : {m_noze_min:.2f}")
    print(f"m_dot_cor_min :{m_dot_co[arg_max]:.2f}, delta_dot_max : {delta_dot_max:.2f}, m_noze : {m_s_max:.2f}, delta_dot_mid : {m_noze_max:.2f}")

    print(f"m_dot_cor_mid : {m_dot_co[arg_mid]:.2f}, m_s : {m_s:.2f}, m_noze : {m_noze:.2f}, delta_dot_mid : {delta_dot_mid:.2f}")


    if np.abs(delta_dot_mid) < tol :
        break
    elif np.abs(delta_dot_min) < np.abs(delta_dot_max)  :
        arg_max = arg_mid
    elif np.abs(delta_dot_min) > np.abs(delta_dot_max):
        arg_min = arg_mid
    elif arg_min == arg_max :
        break
    elif delta_dot_max * delta_dot_min < 0 :
        arg_min = arg_max 


    iter += 1







