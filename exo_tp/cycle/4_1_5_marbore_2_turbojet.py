# The Marbore II turbojet engine consists of a single stage radial compressor (3), followed by an annular combustion
#  chamber (7), a single stage axial turbine (10) and finally a converging nozzle (11). We denominate the following
#  stations
#  • ambient conditions (a)
#  • compressor inlet (1)
#  • compressor outlet/combustion chamber inlet (2)
#  • combustion chamber outlet/turbine inlet (3)
#  • turbine outlet (4)
#  • nozzle outlet (5)
#  From the data sheets we know that at the nominal point at SLS
#  • the design pressure ratio is Πc = 4;
#  • the rotation speed is n = 21600 rpm;
#  • the design air mass flow rate is ˙ma = 7.6 kg/s;
#  • the fuel mass flow rate is ˙mf = 0.1191 kg/s;
#  • the fuel lower heating value is ∆hf = 42.7 MJ/kg;
#  • the turbine inlet temperature is TIT = 800◦C;
#  • the turbine has a total-to-total isentropic efficiency ηs,t = 0.8.


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

isa_sea_lvl = ISA_condition(0)
pressure_ratio = 4
rpm = 21600 # rpm 
m_air = 7.6 
m_fuel = 0.1191
fuel_lower_heating = 42.7 * 10**6
TiT_chamber = 800 + 273.15
eta_turbine_isentro = 0.8

# first phase ambiante condition 
T_2, CP12 = compute_temperature_before_chamber(m_air, m_fuel,TiT_chamber,isa_sea_lvl.T0_r,1000, fuel_lower_heating, 1)

print("T_2                  : \t", T_2)
print("CP                   : \t",CP12)
# Hypothese that 
#  The heat capacity of the incoming air is also applicable to
#  the compression since T◦
#  1 = Tr = 288 K such that the average heat capacity in the compressor is the same as use
print("T_1                   : \t",isa_sea_lvl.T0_r)
gamma12 = findGamma_indec(CP12, isa_sea_lvl.R)

eta_s_c = compute_iso_compressor(4, 1, isa_sea_lvl.T0_r, T_2, gamma12)
print("efficiency combustion : \t", eta_s_c)
# Power conception 
Power_compressor = compute_power_compressor(m_air, CP12, isa_sea_lvl.T0_r, T_2)
print("Power compressor : \t", Power_compressor)

# pressure after turbine --> T3 -- T4 if no shaft so nothing loss between the compressor and the turbine 

T4, Cp_3_4 = compute_temp_turbine(TiT_chamber, Power_compressor, m_air, m_fuel, 1000)

print("T4               : \t", T4)
p4 = pressure_turbine(TiT_chamber, T4, eta_turbine_isentro,Cp_3_4, isa_sea_lvl.R,1)
print("Turbine outlet pressure: ", p4)