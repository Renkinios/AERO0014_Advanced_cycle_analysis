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

# Determine the

# 1. the compressor isentropic eﬃciency ⌘s,c;

# 2. the power consumption of the compressor Pc;

# 3. the total pressure after the turbine p

# 4;

# 4. the thrust T and speciﬁc fuel consumption SFC;

# 5. the thermal and propulsive eﬃciencies ⌘T resp. ⌘p.


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
m_air = 7.6 
fuel_mass_flow = 0.1191 
fuel_lower_heat = 42.7 *10**6
Temperature_inlet = 800 + 273.15
turbine_eff = 0.8

# 1) comp eff 

isa_sea_lvl = ISA_condition(0, isa = False)
T0 = isa_sea_lvl.T0
P0 = isa_sea_lvl.P0

T1  = T0
P1  = P0  # the motor is at rest so don't increase inertia


# ambiant condition

# compressor inlet (1)
# comp outlet can considering like a group 

# chamber inlet (2)
T2, cp2 = compute_temperature_before_chamber(m_air, fuel_mass_flow, Temperature_inlet, isa_sea_lvl.R, 1000, fuel_lower_heat, 1)

T1 = isa_sea_lvl.T0_r #  --> same CP like T_ref = T_1 like sea lvl and rest

gamma2 = findGamma_indec(cp2, isa_sea_lvl.R)
P2 = ratio_c_p * P1

# compressor
eff_iso_c =  compute_iso_compressor(ratio_c_p,1, T1, T2, gamma2)

power_comp = compute_power_compressor(m_air, cp2, T1, T2)


print("eeff_iso_c : ", eff_iso_c)

# like no lost for the power --> we can say 
power_turb = power_comp

# chamber no lsot 
P3 = P2
T3 = Temperature_inlet
# turbine
T4 ,Cp4 = compute_temp_turbine(T3, power_turb, m_air, fuel_mass_flow, 1000)

gamma4 = findGamma_indec(Cp4, isa_sea_lvl.R)

P4 = pressure_turbine(T3, T4, turbine_eff, Cp4, isa_sea_lvl.R, P3)

print_stat(P4, T4, "Turbine")

# nozzle
Trust = trust_nozzle_all(1.38, T4, P4, m_air, fuel_mass_flow, 0, isa_sea_lvl)
SFC = fuel_mass_flow / Trust * 3600 *10
print("SFC without conv : ", SFC)
print("fuel_mass_flow : ", fuel_mass_flow)
print_stat(T4, P4, "Nozzle")
print_trust(Trust)
print_SFC(SFC)



