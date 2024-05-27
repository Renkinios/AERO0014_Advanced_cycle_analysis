# The Marbore II turbojet engine consists of a single stage radial compressor (3), followed by an annular combustion chamber (7), a single stage axial turbine (10) and ﬁnally a converging nozzle (11). We denominate the following stations

# • ambient conditions (a)

# • compressor inlet (1)

# • compressor outlet/combustion chamber inlet (2)

# • combustion chamber outlet/turbine inlet (3)

# • turbine outlet (4)

# • nozzle outlet (5)


# 1.1 Gas turbine cycle at sea level (5 points)

# From the data sheets we know that at the nominal point at SLS

# • the design pressure ratio is ⇧c =4;

# • the rotation speed is n = 21600 rpm;

# • the design air mass ﬂow rate is ˙ma =7.6 kg/s;

# • the fuel mass ﬂow rate is ˙mf =0.1191 kg/s;

# • the fuel lower heating value isHf = 42.7 MJ/kg;

# • the turbine inlet temperature is TIT = 800C;

# • the turbine has a total-to-total isentropic eﬃciency ⌘s,t =0.8.

# The Marbore II powers an aircraft ﬂying at M =0.65 and altitude of 9000 m in standard conditions. Assume the compressor is operating in full similarity with the nominal point on the ground. The fuel mass ﬂow is regulated such that turbine inlet temperature is maintained at T

# 3 = 800. We further asssume the

# turbine eﬃciency is still the same. Determine

# 1. the air mass ﬂow rate ˙ma and the shaft rotation speed n;

# 2. total pressure and temperature after the compressor p

# 2, T

# 2;

# 3. the compressor power Pc;

# 4. fuel mass ﬂow rate ˙mf;

# 5. the thrust and speciﬁc fuel consumption T and SFC; 6. the thermal and propulsive eﬃciency ⌘T and ⌘p.


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

ratio_c_p = 4
RPM = 21600 
fuel_lower_heat = 42.7 *10**6
Temperature_inlet = 800 + 273.15
turbine_eff = 0.8
M = 0.65 
isa_9000 = ISA_condition(9000, True)
isa_9000.P0 = 30742.5
isa_9000.T0 = 229.65
isa_sea_lvl =ISA_condition(0, False)
speed_v_0 = mac_number2speed(isa_9000.gamma_index, isa_9000.R, isa_9000.T0, M)

# ambiant condition 

T1, P1 = ambiante_condition(isa_9000.gamma_index, M, isa_9000.T0, isa_9000.P0)
print_stat(P1, T1, "Ambiant condition")
m_air =  7.6 * P1/isa_sea_lvl.P0 * np.sqrt(isa_sea_lvl.T0/T1)
print("Air mass flow rate : ",m_air," [kg/s]")
gamma = findGamma_indec(isa_9000.C_P, isa_9000.R)

T2 = 421.365
P2 =163340
power_compresseur = 571.667 * 10**3

print_stat(P2, T2, "Compressor outlet")

# chamber combustion

m_fuel = mass_flow_chamber(m_air,T2,Temperature_inlet,isa_9000.T0_r, 1, fuel_lower_heat, 0.03)

T3 = Temperature_inlet
P3 = P2
print_stat(P3, T3, "Combustion chamber")
print_mass_flow(m_fuel)

# turbine

power_turbine  = power_compresseur

T4, CP4= compute_temp_turbine(Temperature_inlet, power_turbine, m_air, m_fuel, T3)
P4 = pressure_turbine(Temperature_inlet, T4, turbine_eff, CP4, isa_9000.R, P3)

print_stat(P4, T4, "Turbine")

Trust = trust_nozzle_all(1.38, T4, P4, m_air, m_fuel, speed_v_0, isa_9000)
SFC = m_fuel / Trust 

print_stat(T4, P4, "Nozzle")
print_trust(Trust)
print_SFC(SFC)






