#  The turbojet examined in Exercise 4.1.2 is now equipped with an afterburner having a combustion efficiency of 89%
#  and causing a total pressure loss of 3%.
    #  1. Determine the thrust specific fuel consumption and the thrust when the total temperature of the exhaust
    #  gases is 1778 K with afterburning andx assuming a convergent nozzle.
    #  2. As in Exercise 4.1.2, examine how the aformentioned parameters would change if a converging-diverging nozzle
    #  was installed.
    #  3. Compare these two results with the ones obtained in Exercise 4.1.2 without afterburner.

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

# Following of the exo 4_1_2 

M = 0.75
isa_sea_lvl = ISA_condition(0,False)
m_air = 165 # [lb/s]
m_air = convmass(m_air,'lbm','kg')
Pi_c = 15      # pressure ratio
eta_c_s = 0.88 # isentropic efficiency compressor

heating_value = 17800 # [BTU/lb]
heating_value = convenergy(heating_value,'BTU','J')
heating_value = convmass(heating_value,'kg','lbm') # [J/kg]


T_exit_cc = 2500 # [R]
T_exit_cc = convtemp(T_exit_cc,'R','K') # temperature sortie chambre de combuston


eta_cc = 0.98 # efficasite cahmbre combustion
Pi_cc = 0.95 # compression chambre combustion

eta_t_s = 0.915 # efficieny turbine

# Converging nozzle
RR = 0.92 # recovery in the inlet
eta_m = 0.995 # shaft efficiency

# first step determine the speed v_0
speed_0 = mac_number2speed(isa_sea_lvl.gamma_index, isa_sea_lvl.R, isa_sea_lvl.T0, M)



# Atmpspheric conditions
T1, P1 = ambiante_condition(isa_sea_lvl.gamma_index, M, isa_sea_lvl.T0, isa_sea_lvl.P0)


# Intake
T2, P2 = intake(RR,T1,P1)

# Compressor
P3  = Compute_press_output(Pi_c, P2)

# gamma_3 is not given so need to do a processue iterative to find it
poly_eff = eff_poly2eff_iso_compressor(Pi_c, isa_sea_lvl.gamma_index, eta_c_s)
gamma, Cp, T3 = compute_tot_isentropic_eff_compressor(poly_eff,1.38,Pi_c,T2,isa_sea_lvl.R)
power_compress = compute_power_compressor(m_air, Cp, T2, T3)


# Combustion chamber determine the mass fuel that we need
m_fuel = mass_flow_chamber(m_air,T3,T_exit_cc,isa_sea_lvl.T0_r ,eta_cc,heating_value,0.02)
T4 = T_exit_cc
P4 = Compute_press_output(Pi_cc, P3)



# Turbine 
Power_produce = power_produce_turbine(power_compress,eta_m)
T5, Cp_5_6    = compute_temp_turbine(T4,Power_produce,m_air,m_fuel,1000)
P5            = pressure_turbine(T4, T5, eta_t_s, Cp_5_6, isa_sea_lvl.R, P4)


# 1 ) 
# Determine the thrust specific fuel consumption and the thrust when the total temperature of the exhaust
# gases is 1778 K with afterburning andx assuming a convergent nozzle

T6 = 1778 # [K]
eff_afterburner  = 0.89
loss_afterburner = 0.03

P6                   = Total_pressure_combustion(loss_afterburner,P5)
mass_flow_after_burn = mass_flow_chamber_afterburn(m_air,m_fuel, T5, T6, isa_sea_lvl.R, eff_afterburner, heating_value)
print("Pressure after burn           : \t", P6/10**3, "[KPa]")
print("Mass flow after burn          : \t", mass_flow_after_burn, "[kg/s]")

# Convergence nozzle

gamma, T7_Static    = compute_nozzle_converging_pressure_ratio_phi_n(1.38, T6, m_air, m_fuel + mass_flow_after_burn, isa_sea_lvl.R)
print("Gamma nozzle                  : \t", gamma)
print("Temperature nozzle            : \t", T7_Static, "[K]")

shock               = compute_nozzle_converging_pressure_ratio_prime(gamma, P6, isa_sea_lvl.P0)
A7, P_7_static, V7  = compute_nozzle_converging_area(gamma, isa_sea_lvl.R, T7_Static, P6, mass_flow_after_burn + m_air + m_fuel) 
print("P_7_static                   : \t", P_7_static/10**3, "[KPa]")
print("V7                           : \t", V7, "[m/s]")
print("A7                           : \t", A7, "[m^2]")
Trust               = compute_thrust(V7, m_air, m_fuel, speed_0, P_7_static, isa_sea_lvl.P0, A7, shock)
SFC                 = compute_specific_fuel_consumption(m_fuel + mass_flow_after_burn, Trust)

print("Trust                          : \t", Trust/10**3, "[kN]")
print("Specific fuel consumption      : \t", SFC, "[kg/N.s]")

# 2 )
# As in Exercise 4.1.2, examine how the aformentioned parameters would change if a converging-diverging nozzle

print("############### Converging-diverging nozzle #################")
V_10 = compute_mach_exhaust(P6, isa_sea_lvl.P0 ,1.38, T6, m_fuel + mass_flow_after_burn, m_air, isa_sea_lvl.R)
Trust = compute_thrust(V_10, m_air, m_fuel + mass_flow_after_burn, speed_0, P6, isa_sea_lvl.P0, 0, 0)
SFC = compute_specific_fuel_consumption(m_fuel + mass_flow_after_burn, Trust)

print("Trust                      : \t",Trust/10**3," [N]")
print("Specific fuel consumption  : \t",SFC," [kg/N.s]")