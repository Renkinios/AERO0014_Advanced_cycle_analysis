import numpy as np
from unit import *
from ISA import *
from cycle.ambiante_condition import *
from cycle.comb_chamber import *
from cycle.Intake import *
from cycle.compressor import *
from cycle.turbine import *
from cycle.exhaust import *


# Compute the iffernt mode of a cycle
# Station 0 : Ambiante condition 
# Station 1 : Intake
# Station 2 : LPC
# Station 3 : HPC
# Station 4 : Combustion chamber
# Station 5 : HPT
# Station 6 : LPT
# Station 7 : Afterburner
# Station 8 : Nozzle
# Station 9 : Nozzle throat
# Station 10 : Nozzle exhaust


# Ambiante condition 
Altitude = 57400 # ft
Altitude = convlength(Altitude,'ft','m')

speed      = 550   # mph
speed      = convspeed(speed,'mph','m/s')
Temp_isa   = ISA_condition(Altitude,True)
Mac_number = compute_mac_number(Temp_isa.gamma_index, Temp_isa.R, Temp_isa.T0, speed)


T1, P1 = ambiante_condition(Temp_isa.gamma_index, Mac_number, Temp_isa.T0, Temp_isa.P0)

print(" ####################### Ambiante condition ####################### ")
print("Altitude               : \t",Altitude," [m]")
print("Maximum temperature    : \t",T1," [K]")
print("Maximum pressure       : \t",P1/10**3," [kPa]")
print("Temperature isa        : \t",Temp_isa.T0," [K]")
print("Pressure isa           : \t",Temp_isa.P0/10**3," [kPa]")
print("Speed                  : \t",speed," [m/s]")
print("Mac number             : \t",Mac_number)
      
      
print(" ####################### Intake condition ####################### ")

RR = 0.98
T_2, P_2 = intake(RR,T1,P1)
print("Intake temperature        : \t",T_2," [K]")
print("Intake pressure           : \t",P_2/10**3," [kPa]")

print(" ####################### Compression Low pressure condition ####################### ")
# isentropic compressor 
Pi_LPC                 = 0.91
gamma_start_LPC        = 1.4 
compression_factor_LPC = 2.3
R                      = 287.058 # J/kg.K

gamma_lpc, Cp_lpc, T3 = compute_tot_isentropic_eff_compressor(Pi_LPC, gamma_start_LPC, compression_factor_LPC, T_2, R)
P3 = compression_factor_LPC * P_2
print("Gamma                     : \t",gamma_lpc)
print("Cp                        : \t",Cp_lpc)
print("Total temperature         : \t",T3, "[K]")
print("Pressure                  : \t",P3/10**3," [kPa]")

mass_flow_air      = 56   # [kg/s]

Power_comp_lpc = compute_power_compressor(mass_flow_air, Cp_lpc, T_2, T3)
print("Power compressor           : \t",Power_comp_lpc)


print(" ####################### Compression High pressure condition ####################### ")
# isentropic compressor
Pi_HPC                 = 0.91
gamma_start_HPC        = 1.38
compression_factor_gen = 9.5
compression_factor_HPC = compression_factor_gen / compression_factor_LPC

gamma_hpc, Cp_hpc, T4 = compute_tot_isentropic_eff_compressor(Pi_HPC, gamma_start_HPC, compression_factor_HPC, T3, R)
P4 = P3 * compression_factor_HPC
print("Gamma CHP                 : \t",gamma_hpc)
print("Cp CHP                    : \t",Cp_hpc, "[J/kg.K]")
print("Total temperature CHP     : \t",T4, "[K]")
print("Pressure CHP              : \t",P4/10**3," [kPa]")


Power_comp_hpc = compute_power_compressor(mass_flow_air, Cp_hpc, T3, T4)

print("Power compressor CHP      : \t",Power_comp_hpc)

print(" ####################### Combustion chamber condition ####################### ")
# Combustion chamber
TIT = 1040 +273.15 #  Turbine Inlet Temperature [K]
T5  = TIT
comb_chamber_pressur_loss = 0.03

P5  = Total_pressure_combustion(comb_chamber_pressur_loss,P4)

print("Temperature chambre       : \t",T5, "[K]")
print("Pressure chamber          : \t",P5/10**3, "[kPa]")

# TiT           = T4
# ToT           = 
Ref_temp      = 288.15 #[K]
Comb_eff      = 0.98
FuelLowerHeat = 42.8 * 10**6
Starf         = 0.05

mass_flow_fuel = mass_flow_chamber(mass_flow_air,T4,T5,Ref_temp,Comb_eff,FuelLowerHeat,Starf)
print("Mass flow fuel            : \t",mass_flow_fuel, "[kg/s]")

print(" ####################### High Pressure Turbine ####################### ")

meca_eff_shaft_high = 0.995

power_hpt = power_produce_turbine(Power_comp_hpc,meca_eff_shaft_high)

print("Power High Pressure Turbine : \t",power_hpt/10**6,"[MW]")
T_6_first_guess  = 1000 
T6, CP_5_6 = compute_temp_turbine(T5, power_hpt, mass_flow_air, mass_flow_fuel, T_6_first_guess)

print("Temperature High Pressure Turbine : \t",T6,"[K]")
eta_isentropic_HPT = 0.93
P6  = pressure_turbine(T5, T6, eta_isentropic_HPT, CP_5_6, R, P5)
print("Pressure Low Pressure Turbine     : \t", P6/10**3, "[KPa]")

print(" ####################### Low pressure turbine ####################### ")

meca_eff_shaft_low = 0.995

power_hpt_low = power_produce_turbine(power_hpt,meca_eff_shaft_low)
print("Power Low Pressure Turbine : \t",power_hpt_low/10**6,"[MW]")

T_7_first_guess  = 1000 
T7, CP_6_7 = compute_temp_turbine(T6, power_hpt_low, mass_flow_air, mass_flow_fuel, T_7_first_guess)
print("Temperature Low Pressure Turbine : \t",T7,"[K]")

eta_isentropic_LPT = 0.93
P7  = pressure_turbine(T6, T7, eta_isentropic_HPT, CP_6_7, R, P6)
print("Pressure Low Pressure Turbine    : \t", P7/10**3, "[KPa]")


print("######################## Dry mode #########################")
print(" ####################### Afterburner ####################### ")

print(" ####################### Nozzle ####################### ")




V_10 = compute_mach_exhaust(P7, Temp_isa.P0 ,1.4, T7, mass_flow_fuel, mass_flow_air, R)
print("Pressure Low Pressure Turbine    : \t", P7/10**3, "[KPa]")

print("Exaust speed                     : \t", V_10, "[m/s]")
trust = compute_thrust(V_10, mass_flow_air, mass_flow_fuel, speed,P7, P7,0, 0)
print("Trust                            : \t",trust/10**3, "[kN]")
SFC = compute_specific_fuel_consumption(mass_flow_fuel, trust)
print("Specific fuel consumption        : \t",SFC, "[kg/N.s]")

print("####################### WET mode #######################")
print(" ###################### Afterburn ####################### ")

aftern_burn_pressure_loss = 0.06
aftern_burn_comb_eff      = 0.91
start_cp                  = 1000
m_after_burn              = 2.5


T8  = compute_temperature_afterburn_Wet(mass_flow_air ,mass_flow_fuel, m_after_burn, T7, Ref_temp, start_cp, aftern_burn_comb_eff, FuelLowerHeat)

print("Temperature afterburner          : \t", T8, "[K]")

P8  = Total_pressure_combustion(aftern_burn_pressure_loss,P7)
print("Pressure afterburner             : \t", P8/10**3, "[kPa]")
print(" ####################### Nozzle ####################### ")

V_10 = compute_mach_exhaust(P8, Temp_isa.P0 ,1.38, T8, mass_flow_fuel + m_after_burn, mass_flow_air, R)
print("Speed exhaust                    : \t", V_10, "[m/s]")

trust = compute_thrust(V_10, mass_flow_air, mass_flow_fuel + m_after_burn, speed, P7, P7,0, 0)
print("Trust                            : \t",trust/10**3, "[kN]")

SFC = compute_specific_fuel_consumption(mass_flow_fuel + m_after_burn, trust)
print("Specific fuel consumption        : \t",SFC, "[kg/N.s]")














