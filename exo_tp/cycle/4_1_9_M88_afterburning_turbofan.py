# The Snecma M88 engine is a two-spool afterburning turbofan, powering the Rafale fighter. The cutaway in figure
# 4.5a shows it consists of a 3-stage LP and 6-stage HP compressor (LPC resp. HPC), driven by dedicated single stage
# turbines (LPT resp. HPT). The secondary flow is mixed with the primary flow after the LP turbine before entering
# the afterburner. The air leaving the afterburner is ejected through a converging nozzle with variable cross-section.
# Figure 4.5b shows a conceptual drawing of the engine architecture.
# The aim of the exercise is to provide an educated guess of the main performance parameters and conditions in
# the cycle at ground conditions for both dry and wet operation, using reasonable assumptions, tables providing Cp as
# a function of temperature and fuel-to-air-ratio, as well as the fuel lower heating value Δhf = 42.8 MJ/kg. We
# denominate the stations of the cycle as follows
# 1 upstream of the LP compressor
# 2 downstream of the LPC / upstream of the HPC / inlet of the secondary flow duct;
# 3 downstream of the HPC / inlet of the combustion chamber;
# 4 outlet of the combustion chamber / inlet of the HPT;
# 5 outlet of the LPT / primary inlet of the mixer ;
# 5’ outlet of the secondary duct / secondary inlet of the mixer;
# 6 outlet of the mixer / inlet of the afterburner;
# 7 outlet of the afterburner / entry of the nozzle;
# 8 nozzle outlet.
# The following assumptions are made:
# • the total pressures of primary and secondary flows entering the mixer/afterburner are exactly equal;
# • the polytropic efficiency of all compressor stages is estimated to be ηp,c = 0.8;
# • the turbine overall isentropic efficiencies (over both LPT and HPT) is ηs,t = 0.90;
# • the total pressure loss over the secondary flow between the LPC and the mixer is 1% with respect to the total
# pressure after the LPC;
# • the combustion chamber total pressure loss is 3% while the combustion efficiency is 100%;
# • the mixing total pressure loss is estimated at 3% with respect to the common total pressure at the mixer inlet;
# • when activated, the afterburner introduces an additional total pressure loss of 2% with respect to the upstream
# value;
# 54/162
# For simplicity
# • you can assume that during the compression of the secondary flow in the LPC the heat capacity of the air
# does not change.
# • however, the change of the heat capacity has to be taken into account for the compression of the primary flow;
# a single value is to be taken over both LPC and HPC.
# • the polytropic efficiency is the same in all stages in the LP and HP compressor;
# • as suggested by the numbering of the stations, you can compute the turbines together, to provide the combined
# power of both LPC and HPC;
# • you may determine the total temperature after mixing by a simple mass-weighted average.
# It is highly recommended to use a script.
# Questions
# • Estimate the nominal operating point in dry operation in ground conditions. The turbine inlet
# temperature does not reach the maximum, but is measured to be TiT = T◦
# 4 = 1560 K. Compute
# – the total conditions at all stations in the cycle;
# – the isentropic efficiencies and absorbed power for both the LPC and HPC;
# – estimate the thrust and compare to the data sheet;
# – the area of the exhaust nozzle.
# • The afterburner is activated and the nozzle is opened such that the operation point of the gas turbine
# cycle as well as the mixer is unmodified with respect to dry operation. Compute the conditions in the
# afterburner and the corresponding variation of the outlet nozzle section. Update the estimate of the
# thrust.


#                                                 dry     wet          [units]
# overall pressure ratio Π                            24.5                -
# air mass flow rate m˙ a                              65               [kg/s]
# bypass ratio α                                     0.3:1.0              -
# maximum turbine inlet temperature TiTmax            1850               [K]
# thrust specific fuel consumption SFC            0.8     1.70        [kg/daN.h]
# thrust T                                        11250   16860         [lbf]

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

hating_fuel_value = 42.8 * 1**6  # [J/kg]



# We have the trust so we going to part on this value
T_dry = 11250  # [lbf]
T_dry = convforce(T_dry, 'lbf', 'N')  # [N]

T_wet = 16860  # [lbf]
T_wet = convforce(T_wet, 'lbf', 'N')  # [N]

SFC_wet = 1.70  # [kg/daN.h]
SFC_wet = 1.7/10/3600  # [kg/N.s]

SFC_dry = 0.8  # [kg/daN.h]
SFC_dry = 0.8/10/3600  # [kg/N.s]

m_fuel_wet =  T_wet * SFC_wet  # [kg/s]
m_fuel_dry =  T_dry * SFC_dry  # [kg/s]

m_fuel_afterburner = m_fuel_wet - m_fuel_dry  # [kg/s]

# We have the bypass ratio so we can calculate the mass flow rate of the air
alpha = 0.3  # [-] factor of the bypass ratio separation between the primary and secondary flow m_entrance

m_air = 65  # [kg/s] --> composossé entrance and sortance of the engine

m_entrance = m_air/(1 + alpha)  # [kg/s]
m_sortance = m_air - m_entrance  # [kg/s]


# engine is stasionnaire. 

isa_0 = ISA_condition(0) 
T0 = isa_0.T0  # [K]
P0 = isa_0.P0  # [Pa]

P1 = P0
T1 = T0 # like don't have a 

# Compressor
comp_factor = 24.5
P4 = comp_factor * P0  # [Pa] total pressure at the exit of the compressor --> considere the HPT and LPT

poly_comp = 0.8  # [-] polytropic efficiency of the compressor
# gamma23, Cp23, T3 = compute_tot_isentropic_eff_compressor(0.8, 1.4, comp_factor,T_2, isa_0.R)
# power_comp = compute_power_compressor(m_entrance, Cp23, T_2, T3)  # [W] power absorbed by the compressor


################## Comb chamber ####################

pressure_loss_chamber = 0.03
P4 = Total_pressure_combustion(pressure_loss_chamber, P1)  # [Pa] total pressure at the exit of the combustion chamber
T4 = 1560  # [K] turbine inlet temperature


print("m_entrance \t:", m_entrance)
T3, CP3 = compute_temperature_before_chamber(m_entrance, m_fuel_dry, T4, isa_0.T0_r, 1000, hating_fuel_value)  # [K] temperature at the exit of the compressor

#  Assume that the gamma is the same for all the compression we can converte the eta_p_c in eta_s_c

gamma_c = findGamma_indec(CP3, isa_0.R)
eff_s_c = eff_poly2eff_iso_compressor(comp_factor, gamma_c, poly_comp)  # [-] isentropic efficiency of the compressor

# goal sea the comrpessor and the turbine with = power like no shaft 



print("T3 \t:", T3)
print("CP3 \t:", CP3)

ratio_p_old_low  = 0
ratio_p_beging_low = 1
iter = 0
max_iter = 100
tol = 1e-4
# considere le meme gamma du xou 
while iter < max_iter and  np.abs((ratio_p_old_low - ratio_p_beging_low)/ratio_p_beging_low) < tol:
    ratio_p_old_low = ratio_p_beging_low
    T_2_guess = compute_Temp_iso(comp_factor, 1, T1, gamma_c)
    T_3_guess = compute_Temp_iso(comp_factor, 1, T_2_guess, gamma_c)
    work_comp = m_air * (CP3 * (T_2_guess - T1)) -  m_entrance *( CP3 * (T3 - T_2_guess))
    work_turb = work_comp / (m_entrance + m_fuel_dry)
    p_5_guess = 0.99 * ratio_p_beging_low * P1
    work_turb = comp_work_turbine(CP3, T4, P4/p_5_guess, eff_s_c, gamma_c) 
    iter += 1

# ... error 

################## Turbine ####################

# rattio melangeur 

# P5 = P2 * 0.99 

############# Melangeur ###################
# Same pression before and after  so  p5' = p5 and --> p5' = p2 * 0.99 



