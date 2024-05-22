#  A turbojet flies at sea level, Mach M = 0.75 (ISA). It ingests ˙ma = 165 lb/s of air. The compressor operates at
#  a pressure ratio of πc = 15 and an isentropic efficiency of ηc,s = 0.88. The fuel lower heating value and burner
#  total exit temperature are respectively ∆hf = 17800 BTU/lb and Texit cc = 2500◦R. The burner has an efficiency
#  of ηcc = 0.98 and a total pressure ratio of πcc = 0.95, whereas the turbine has an efficiency of ηt,s = 0.915. A
#  converging nozzle is used. The total pressure recovery in the inlet is RR = 0.92 and the shaft efficiency is ηm = 99.5.
#  • Find the developed thrust and TSFC and provide the nozzle throughflow section.
#  • How (much) would the thrust and TSFC change when replacing the convergent nozzle with an adapted
#  convergent-divergent nozzle? Is it interesting to install this type of nozzle for the examined operating point?
#  Find γ by iteration using the Cp(T) charts.

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


M = 0.75
isa_sea_lvl = ISA_condition(0,False)
m_air = 165 # [lb/s]
m_air = convmass(m_air,'lbm','kg')
Pi_c = 15      # pressure ratio
eta_c_s = 0.88 # isentropic efficiency compressor

heating_value = 17800 # [BTU/lb]
heating_value = convenergy(heating_value,'BTU','J')
heating_value = convmass(heating_value,'kg','lbm') # [J/kg]
print("Heat",heating_value)

T_exit_cc = 2500 # [R]
T_exit_cc = convtemp(T_exit_cc,'R','K') # temperature sortie chambre de combuston
print("T_exit_cc",T_exit_cc)

eta_cc = 0.98 # efficasite cahmbre combustion
Pi_cc = 0.95 # compression chambre combustion

eta_t_s = 0.915 # efficieny turbine

# Converging nozzle
RR = 0.92 # recovery in the inlet
eta_m = 0.995 # shaft efficiency

# first step determine the speed v_0
speed_0 = mac_number2speed(isa_sea_lvl.gamma_index, isa_sea_lvl.R, isa_sea_lvl.T0, M)

print("############## Ambiante Condition #########################")

# Atmpspheric conditions
T1, P1 = ambiante_condition(isa_sea_lvl.gamma_index, M, isa_sea_lvl.T0, isa_sea_lvl.P0)

print("Altitude               : \t",0," [m]")
print("Maximum temperature    : \t",T1," [K]")
print("Maximum pressure       : \t",P1/10**3," [kPa]")

# Intake
T2, P2 = intake(RR,T1,P1)

print("############## Intake Condition #########################")
print("Intake temperature        : \t",T2," [K]")
print("Intake pressure           : \t",P2/10**3," [kPa]")

# Compressor
P3  = Compute_press_output(Pi_c, P2)



# gamma_3 is not given so need to do a processue iterative to find it
poly_eff = eff_iso2eff_poly(Pi_c, isa_sea_lvl.gamma_index, eta_c_s)
gamma, Cp, T3 = compute_tot_isentropic_eff_compressor(poly_eff,1.38,Pi_c,T2,isa_sea_lvl.R)
power_compress = compute_power_compressor(m_air, Cp, T2, T3)

print("############## Compressor Condition #########################")
print("Gamma                     : \t",gamma)
print("Cp                        : \t",Cp)
print("Total temperature         : \t",T3, "[K]")
print("Pressure                  : \t",P3/10**3," [kPa]")

# Combustion chamber determine the mass fuel that we need
m_fuel = mass_flow_chamber(m_air,T3,T_exit_cc,isa_sea_lvl.T0_r ,eta_cc,heating_value,0.02)
T4 = T_exit_cc
P4 = Compute_press_output(Pi_cc, P3)

print("############## Combustion Chamber Condition #########################")
print("Mass flow fuel            : \t",m_fuel," [kg/s]")
print("Total temperature         : \t",T4, "[K]")
print("Pressure                  : \t",P4/10**3," [kPa]")


# Turbine 
Power_produce = power_produce_turbine(power_compress,eta_m)
T5, Cp_5_6    = compute_temp_turbine(T4,Power_produce,m_air,m_fuel,1000)
P5            = pressure_turbine(T4, T5, eta_t_s, Cp_5_6, isa_sea_lvl.R, P4)

print("############## Turbine Condition #########################")
print("Total temperature         : \t",T5, "[K]")
print("Pressure                  : \t",P5/10**3," [kPa]")

# Nozzle exaust

gamma, T6_Static =  compute_nozzle_converging_pressure_ratio_phi_n(1.38, T5, m_air, m_fuel, isa_sea_lvl.R)
shock = compute_nozzle_converging_pressure_ratio_prime(gamma, P5, isa_sea_lvl.P0)
A_ex, P6_static, speed_end_cycle = compute_nozzle_converging_area(gamma, isa_sea_lvl.R, T6_Static, P5, m_air + m_fuel)
Trust    = compute_thrust(speed_end_cycle, m_air, m_fuel, speed_0, P6_static, isa_sea_lvl.P0, A_ex, shock) 
SFC_simple = compute_specific_fuel_consumption(m_fuel, Trust)
print("############## Nozzle Condition #########################")
print("Trust                     : \t",Trust," [N]")
print("Speed end cycle           : \t",speed_end_cycle," [m/s]")
print("Area nozzle               : \t",A_ex," [m^2]")
print("Specific fuel consumption : \t",SFC_simple," [kg/h/daN]")


print("############### Converging-diverging nozzle #################")
# Converging-diverging nozzle the pressure didn't change but the mach change 

V_10  = compute_mach_exhaust(P5, isa_sea_lvl.P0, 1.38, T5, m_fuel, m_air, isa_sea_lvl.R)
Trust = compute_thrust(V_10, m_air, m_fuel, speed_0, isa_sea_lvl.P0, P5, A_ex, 0)
SFC   = compute_specific_fuel_consumption(m_fuel, Trust)

print("Trust                      : \t",Trust," [N]")
print("Specific fuel consumption  : \t",SFC," [kg/N.s]")





