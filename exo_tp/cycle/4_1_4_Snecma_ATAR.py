# Using the Snecma ATAR 09C turbojet specifications given in Figure 4.2:
# 1. Find the isentropic efficiency of the turbine;
# 2. Calculate the exhaust gas velocity with afterburning and compare with the value presented in the figure in
# appendix;
# 3. Compare the ratios of the net thrust for the conditions with and without afterburner activated. Do the same
# for the specific fuel consumption

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

# Value have on the graphe Temperature
TiT_turbine = 890 
TiT_turbine = convtemp(TiT_turbine,'C','K')

ToT_turbine  = 685
ToT_turbine = convtemp(ToT_turbine,'C','K')


PiT_turbine         = 5.47
PiT_turbine = convpres(PiT_turbine,'bar','Pa')


PoT_turbine         = 2.36
PoT_turbine = convpres(PoT_turbine,'bar','Pa')


V_i_turbine         = 150
V_o_turbine         = 346

# 1) Calcule isentropic efficiency of the turbine.
# gamma = ?  need C_P --> calcule with the temperature and the f

m_fuel = 1.2 
m_air  = 68 
f = m_fuel / m_air
isa_sea_lvl = ISA_condition(0)

Cp = findCp((ToT_turbine + TiT_turbine)/2, f)
gamma = findGamma_indec(Cp, isa_sea_lvl.R)
print("gamma                              : \t", gamma)

eff_turb = compute_eff_iso_turbine(TiT_turbine, ToT_turbine, PiT_turbine, PoT_turbine, gamma)

print("Efficiency turbine                 : \t", eff_turb)

# 2) Compute the exaust gazz velocity afterburn 

p_after_brun = 2.09
p_after_brun = convpres(p_after_brun, 'bar', 'Pa')
temperature_after_burn = 1600
temperature_after_burn = convtemp(temperature_after_burn,'C','K')


# Considere converging nozzle so just need to calculate the a 
m_fuel_after_burn = 2.2
f_after_burn = (m_fuel_after_burn + m_fuel) / m_air

gamma, T7_Static    = compute_nozzle_converging_pressure_ratio_phi_n(1.38, temperature_after_burn, m_air, m_fuel + m_fuel_after_burn, isa_sea_lvl.R)
shock               = compute_nozzle_converging_pressure_ratio_prime(gamma, p_after_brun, isa_sea_lvl.P0)
A7, P_7_static, V7  = compute_nozzle_converging_area(gamma, isa_sea_lvl.R, T7_Static, p_after_brun, m_fuel_after_burn + m_air + m_fuel) 
print("P_5_static                   : \t", P_7_static/10**3, "[KPa]")
print("V5                           : \t", V7, "[m/s]")
print("A7                           : \t", A7, "[m^2]")
# Trust               = compute_thrust(V7, m_air, m_fuel, speed_0, P_7_static, isa_sea_lvl.P0, A7, shock)
# SFC                 = compute_specific_fuel_consumption(m_fuel + m_fuel_after_burn, Trust)




