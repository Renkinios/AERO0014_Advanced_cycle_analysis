#  Analyse a two-spool high-bypass ratio turbofan with separate (i.e. non-mixed) core and fan exhausts at flight
#  Mach 0.30 under standard day conditions at an altitude of 400 ft (second segment climb). The primary airflow of
#  the turbofan amounts to 90 kg/s and the bypass ratio is 6. The fan works at a total pressure ratio of 2.2 and the
#  overall pressure ratio is 36. The gases leaving the combustion chamber have a total temperature of 1680 K, while
#  the total pressure ratio over the latter is 0.95. The combustion efficiency is 99% and the fuel lower heating value
#  equals 41,400 kJ/kg.
#  Both core and bypass nozzles are converging and can be assumed to be lossless. The isentropic efficiency of
#  the fan, compressor and turbines (LPT+HPT) are respectively 92%, 90% and 91%. The ram recovery equals 97%.
#  The shaft mechanical losses are negligible for both shafts. Determine the developed thrust and TSFC. Find γ by
#  iteration using the Cp(T) charts.

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

mach_number = 0.3 # Mach number
altitude = 400 # ft
altitude = convlength(altitude,'ft','m')
isa_400  = ISA_condition(altitude,True)
first_air_flow = 90 # kg/s
by_pass_ratio = 6
fan_pressure_ratio = 2.2
overall_pressure_ratio = 36
TiT = 1680
combustion_chamber_ratio = 0.95
combustion_eff = 0.99
fuel_lower_heating = 41.4 * 10**6
Fan_iso_eff = 0.92
comp_iso_eff = 0.9
high_pres_turb_iso_eff = 0.91
low_pres_turb_iso_eff = 0.91
RR = 0.97
isa_400.P0 = 99869

# start condition 
print("#################### Ambiante condition #################")
v_0 = mac_number2speed(isa_400.gamma_index, isa_400.R, isa_400.T0, mach_number)
print("V_0                              : \t", v_0)
print("Ta                               : \t", isa_400.T0)
print("Pa                               : \t", isa_400.P0)




T0, P0 = ambiante_condition(isa_400.gamma_index, mach_number, isa_400.T0, isa_400.P0)
print("T0                               : \t", T0)
print("P0                               : \t", P0)
print_stat(P0, T0, "Total conidtion")
# inlet 

T1, P1 = intake(RR, T0, P0)
print_stat(P1, T1, "Intake")

# Fan 

P2 = Compute_press_output(fan_pressure_ratio,  P1) 

gamma_12, Cp_12, T2 = compute_tot_isentropic_directly_eff_compressor(Fan_iso_eff, 1.4, fan_pressure_ratio, T1, isa_400.R)

print_stat(P2, T2, " FAN")
m_cont = compute_m_sortant_fan(first_air_flow, by_pass_ratio)
power_fan = compute_power_fan(first_air_flow, m_cont, Cp_12, T1, T2)
print_power(power_fan)

# Compressor
ratio_pressure_comp = overall_pressure_ratio / fan_pressure_ratio

P3 = Compute_press_output(ratio_pressure_comp,  P2)
gamma_23, Cp_23, T3 = compute_tot_isentropic_directly_eff_compressor(comp_iso_eff, gamma_12, ratio_pressure_comp, T2, isa_400.R)

print_stat(P3, T3, "COMPRESSOR")
power_comp = compute_power_compressor(first_air_flow, Cp_23, T2, T3)
print_power(power_comp)

# Combustion chamber

P4 = Compute_press_output(combustion_chamber_ratio,  P3)
m_fuel = mass_flow_chamber(first_air_flow, T3, TiT, isa_400.T0_r, combustion_eff, fuel_lower_heating, 0.01)
T4 = TiT
print_stat(P4, T4, " Combustion Chamber")
print_mass_flow(m_fuel)

# turbine 
# like don't have shaft we can considere all power convert to the turbine

Power_turbine = power_comp + power_fan 
T5,Cp45 = compute_temp_turbine(T4,Power_turbine,first_air_flow,m_fuel, 1000)

P5 = pressure_turbine(T4, T5, low_pres_turb_iso_eff, Cp45, isa_400.R, P4)

print_stat(P5, T5, "Turbine")

print("######################## Nozle ###################")
# Core nozzle
gamma, static_T6 = compute_nozzle_converging_pressure_ratio_phi_n(1.38, T5,first_air_flow, m_fuel, isa_400.R )

shock = compute_nozzle_converging_pressure_ratio_prime(gamma, P5, isa_400.P0)

# like isn't shock need tp compute the mach_number iteratively 

V5, gamma, Cp, mach_number = compute_mach_exhaust(P5, isa_400.P0, 1.38, T5, m_fuel, first_air_flow, isa_400.R )
area, static_pressure, speed_output_fan = compute_nozzle_converging_area_mach(gamma, isa_400.R, isa_400.T0, P5, m_cont, mach_number)
Trust_in = compute_thrust(V5, first_air_flow, m_fuel, v_0, isa_400.P0 ,isa_400.P0, area,shock)

print_speed(V5)
print_mac(mach_number)


# second nozle with the fan that take into account so don't have to
P7 = P2
T7 = T2

# Shock in the nozzle
gamma, static_T7 = compute_nozzle_converging_pressure_ratio_phi_n(1.38, T2, m_cont, 0, isa_400.R)

shock = compute_nozzle_converging_pressure_ratio_prime(gamma, P7, isa_400.P0)

area, static_pressure, speed_output_fan = compute_nozzle_converging_area_mach(gamma, isa_400.R, static_T7, P7, m_cont, 1)

Trust_out = compute_thrust(speed_output_fan, m_cont, 0, v_0, static_pressure, isa_400.P0, area, shock)

Trust = Trust_in + Trust_out

SFC = compute_specific_fuel_consumption(m_fuel, Trust)
print_SFC(SFC)
print_area(area)
print_trust(Trust)

print(" ################## Test ##################")
print(" ############ first trust #############")
trust = trust_nozzle_all(1.38, T5, P5, first_air_flow, m_fuel, v_0, isa_400)
trust_after = trust_nozzle_all(1.38, T2, P2, m_cont, 0, v_0, isa_400)
print_trust(trust + trust_after)


