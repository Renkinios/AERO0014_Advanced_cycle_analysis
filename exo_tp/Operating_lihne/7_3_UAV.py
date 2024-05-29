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


ISA = ISA_condition(0,False)
ISA.T0 = 228.71
ISA.P0 = 30089.6
mac = 0.5
T1, P1 = ambiante_condition(ISA.gamma_index, mac, ISA.T0, ISA.P0)
print_stat(P1, T1, "Ambiante")

RPM = 37780
n_cor = compute_RPM_corrected2RPM(1 ,T1)

RPM_no = RPM/n_cor

# come from graph 
m_dot_np = np.array([2.5, 2.7, 2.8, 2.9, 3])
ratio_pressure_fan = np.array([1.19, 1.19, 1.18, 1.175, 1.15])
eta_s = np.array([0.62, 0.75, 0.82, 0.83, 0.75])

# interpolation
interpol_fan = cubic_splane_interpol(m_dot_np,ratio_pressure_fan)
interpol_eta_s = cubic_splane_interpol(m_dot_np, eta_s)

true_Trust = 71 
Trust_approx = 0
iter_max = 100
iter = 0
tol = 1e-4

v_0 = mac_number2speed(ISA.gamma_index, ISA.R, ISA.T0, mac)
m_dot_np = np.linspace(np.min(m_dot_np), np.max(3), 1000)
Mac_start = 0.7

def trust_7_3(iter,v_0):
    m_flow = compute_massFlow_correct2massFlow(T1, P1, m_dot_np[iter]) 
    P2     = P1 * interpol_fan(m_dot_np[iter])
    gamma, Cp, T2 = compute_tot_isentropic_directly_eff_compressor(interpol_eta_s(m_dot_np[iter]), 1.38, interpol_fan(m_dot_np[iter]), T1, ISA.R)
    # print("T2: ", T2)
    v_j, _, Cp, mach_number, static_temp = compute_mach_exhaust(P2, ISA.P0, gamma, T2, 0, m_dot_np[iter], ISA.R)
    # print("v_j: ", v_j)
    Trust_approx = m_flow *(v_j - v_0)
    return Trust_approx

min_arg, max_arg = 0, len(m_dot_np) - 1
while iter < iter_max  and min_arg <= max_arg:
    # m_flow = (compute_massFlow_correct2massFlow(T1, P1, m_dot_np[iter]) + compute_massFlow_correct2massFlow(T1, P1, m_dot_np[len(m_dot_np)-1]))/2
    # P2     = P1 * interpol_fan(m_dot_np[iter])
    # gamma, Cp, T2 = compute_tot_isentropic_directly_eff_compressor(interpol_eta_s(m_dot_np[iter]), 1.38, interpol_fan(m_dot_np[iter]), T1, ISA.R)
    # # print("T2: ", T2)
    # v_j, gamma, Cp, mach_number, static_temp = compute_mach_exhaust(P2, ISA.P0, gamma, T2, 0, m_dot_np[iter], ISA.R)
    # # print("v_j: ", v_j)
    # Trust_approx = m_flow *(v_j - v_0)
    mid_arg =  (min_arg + max_arg) // 2
    Trust_approx_min = trust_7_3(min_arg,v_0)
    Trust_approx_max = trust_7_3(max_arg,v_0)
    Trust_approx_mid = trust_7_3(mid_arg,v_0)
    if min_arg == max_arg:
        break
    if abs(Trust_approx_mid - true_Trust) < tol:
        break
    if np.abs(true_Trust - Trust_approx_min) < np.abs(true_Trust - Trust_approx_max) : 
        max_arg = mid_arg
    else :
        min_arg = mid_arg
    
    iter += 1
    
print("iter: ", iter)
print("Trust_approx_mid: ", Trust_approx_mid)