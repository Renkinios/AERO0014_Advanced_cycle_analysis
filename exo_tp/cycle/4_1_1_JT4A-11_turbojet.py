# The JT4A-11 engine is operating at its normal rated regime at 25,000 ft on a Boeing 707-320 aircraft (see Figure 4.1).
#  If we assume a complete expansion of the exhaust gases in the nozzle, determine:
#  • The exhaust gas velocity vj
#  • The engine thermal efficiency ηth
#  • The propulsive efficiency ηp
#  • The global efficiency ηg
#  • The thrust specific fuel consumption SFC
#  Do the calculations for a flight Mach number of M0 = 0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7 and 0.8. Assume that the
#  lower heating value of the fuel is ∆hf = 42,979 kJ/kg


import sys
import os

# Chemin absolu du répertoire où se trouve ce script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Chemin du répertoire contenant les fichiers à importer
# parent_dir = os.path.join(current_dir, '..', '..', 'cycle')
direct_dir = os.path.join(current_dir, '..', '..')

# sys.path.append(parent_dir)
sys.path.append(direct_dir)

from basic import *
from ISA import *
from unit import *
from thermo import *

from cycle.exhaust import *



mac_number = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]
altitude = 25000 # [ft]
altitude = convlength(altitude,'ft','m')
ISA_25000 = ISA_condition(altitude,True)
heating_value_full = 42979000 # [J/kg]

# Exposion total on the nozlle 
# find the output in the graph 
# Turst and SFC
T   = np.array([7003, 6833, 6625, 6500, 6479, 6541, 6708, 6958, 7160]) #lbf
T   = convforce(T,'lbf','N')
SFC = np.array([0.73, 0.77 ,0.8, 0.84, 0.86, 0.89, 0.91, 0.94, 0.97])  # kg/h /daN 
SFC = SFC/3600/10  # kg/s/N

m_air = np.array([105, 106, 108, 112, 115, 122, 127, 136, 148]) #lb/s
m_air = convmass(m_air,'lbm','kg')

for i in range(len(T)) : 
    print(" ####################### Mac number : ",mac_number[i]," ####################### ")
    m_fuel = SFC[i] * T[i]
    print("debit mass fuel : \t",m_fuel," [kg/s]")
    speed_0 = mac_number2speed(ISA_25000.gamma_index, ISA_25000.R, ISA_25000.T0, mac_number[i])
    # Exposion total on the nozlle  so p_9 = p_0
    v_outlput = Compute_exaust_velocity_trust(T[i],m_air[i],m_fuel,speed_0)
    print("V_0           : \t",speed_0," [m/s]")
    print("V_exhaust     : \t",v_outlput," [m/s]")
    Q  = compute_heat_Q(m_fuel,heating_value_full)
    print("Q             : \t",Q/10**6," [MW]")
    W  = compute_work_W(m_air[i],speed_0,m_fuel + m_air[i],v_outlput)
    print("W             : \t",W/10**6," [MW]")
    eta_th = thermal_eff(W,Q)
    print("eta_th        : \t",eta_th)
    eta_p = propu_eff(T[i],speed_0,W)
    eta_tot = eta_th *eta_p
    print("eta_p         : \t",eta_p)
    print("eta_tot       : \t",eta_tot)