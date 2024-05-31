# ;  An Airbus A321 powered with two CFM56-5B2 turbofans (non-mixed exhaust configuration) flies at Mach 0.80
# ;  FL350 (ISA). At the top of climb rating, the engine overall pressure ratio OPR is Π = 35.5 and the turbine inlet
# ;  temperature TIT = 1460 K. The other engine parameters are:
# ;  • ram recovery RR = 0.995
# ;  • by-pass ratio α = 5.2
# ;  • fan pressure ratio πf = 1.7 and efficiency ηf = 0.895
# ;  • booster pressure ratio πbooster = 1.8 and efficiency ηbooster,s = 0.875
# ;  • high pressure compressor efficiency ηHPC,s = 0.875
# ;  • combustion pressure loss λcc = 0.06 and efficiency ηcc = 0.999
# ;  • high pressure turbine efficiency ηt,s = 0.91
# ;  • low pressure turbine efficiency ηLPT,s = 0.92
# ; 49/162
# ;  • the mechanical efficiencies of the high pressure and low pressure spool are respectively ηm,HP = 0.995 and
# ;  ηm,LP = 0.995
# ;  It is not needed to iterate on the Cp(T) values, but one may further assume the following values for the thermodynamic
# ;  properties
# ;  • γair = 1.401
# ;  • γfan = 1.400
# ;  • γbooster = 1.399
# ;  • γHPC =1.381
# ;  • ∆hf =42.9 MJ/kg
# ;  • Cp,cc = 1178 J/kg K
# ;  • γHPT =1.305
# ;  • γLPT =1.325
# ;  • γnozzle,bypass = 1.400
# ;  • γnozzle,core = 1.344
# ;  • γnozzle,mixed = 1.397
# ;  With these data :
# ;  1. Quantify the primary airflow when the engine delivers a thrust of 28558 N.
# ;  2. Based on the airflows established in the previous question, determine the performance of the engine in a mixed
# ;  exhaust configuration. Use a perfect mixer (mixing efficiency of 100%).
# ;  Note that in a mixed configuration, the main flow and the by-pass flow are mixed before they are ejected through
# ;  one common nozzle. In the mixer, the static pressures of both flows need to be equal to avoid excessive back flow
# ;  of one of the two streams. This is similar to the Kutta condition in aerodynamics.
# ;  Moreover, in a perfect mixer, the Mach number of both flows are assumed equal, and therefore the total pressure of
# ;  both flows are also the same.

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


RR = 0.995
alpha = 5.2
pressure_ratio_fan = 1.7
efficiency_fan = 0.895
TiT = 1460
overall_pres = 35.5
boster_pres_ratio = 1.8
eff_bister = 0.875
eff_c_s = 0.875
combustion_chabre_loss = 0.06
eff_chamber = 0.999
eff_press_high_turb = 0.91
eff_press_low_turb = 0.92

eff_shaft_HP = 0.995
eff_shaft_LP = 0.995


ISA = ISA_condition(0)
mac = 0.8
ISA.T0 = 218.81
ISA.P0 = 23842.3


# 1) Quantify the primary airflow when the engine delivers a thrust of 28558 N.



Mac = 0.8
speed_0 = mac_number2speed(ISA.gamma_index, ISA.R, ISA.T0, Mac)

def first_part() :
    # Ambiant 
    T1, P1  = ambiante_condition(ISA.gamma_index, mac, ISA.T0, ISA.P0)

    print_stat(P1, T1, "ambiant")
    # Ram recovery 

    T2, P2 = intake(RR, T1, P1)



    gamma, Cp3, T3 = compute_tot_isentropic_directly_eff_compressor(efficiency_fan, 1.4, pressure_ratio_fan, T2, ISA.R)
    # norammly calcule power here 
    P3 = P2 * pressure_ratio_fan
    work_fan = Cp3 *(T3 - T2)

    print_stat(P3,T3, "Fan")


    gamma, Cp4, T4 = compute_tot_isentropic_directly_eff_compressor(eff_bister, 1.38, boster_pres_ratio, T3, ISA.R)
    # norammly calcule power here 

    P4 = P3 * boster_pres_ratio
    work_boster = Cp4 * (T4 - T3)
    print_stat(P4,T4, "Booster")

    overal_prss_comp = overall_pres/boster_pres_ratio/pressure_ratio_fan

    gamma, Cp3, T5 = compute_tot_isentropic_directly_eff_compressor(eff_c_s, 1.381, overal_prss_comp, T4, ISA.R)
    P5 = P4 * overal_prss_comp
    work_high = Cp3 * (T5 - T4)

    print_stat(P5, T5, "Compresseur")


    # chamber 
    P6 = (1 - combustion_chabre_loss) * P5


    T6 = TiT
    print_stat(P6, T6, "chamber")

    CP_cc = 1178 
    entpis_burn = 42.9 *10**6
    f = compute_f_generall(CP_cc, T6, T5, eff_chamber, entpis_burn)


    # turbine --> donc regarder au rapprot de power des  deux --> Pression high

    gamma_turbine = 1.305

    CP7 = - ISA.R * gamma_turbine /(1 - gamma_turbine)

    T7 = - work_high/((1 + f) * CP7 * eff_shaft_HP) + T6

    P7 = pressure_turbine(T6, T7, eff_press_high_turb, CP7, ISA.R, P6)

    print_stat(P7, T7, "High pressure turbine")

    # high turbine 

    gamma_turbine_low = 1.325
    CP8 = - ISA.R * gamma_turbine_low/(1 - gamma_turbine_low)

    T8 =  - ((1 +alpha) * work_fan + work_boster)/(eff_shaft_LP * (1 + f) * CP8) + T7

    P8 = pressure_turbine(T7, T8, eff_press_low_turb, CP8, ISA.R, P7)

    print_stat(P8, T8, "Low pressure turbine")

    return T8, P8, f , T3, P3

# Nozzle Convergent --> two separation two nozzle div

# First part 

# T8, P8, f , T3, P3 = first_part()

# gamma, static_temp = compute_nozzle_converging_pressure_ratio_phi_n(1.38, T8, 1, f, ISA.R)
# shock = compute_nozzle_converging_pressure_ratio_prime(gamma, P8, ISA.P0)

# area, static_pressure, speed_output_fan = compute_nozzle_converging_area_mach(gamma, ISA.R, static_temp, P8, 1 + f, 1)

# print(area)

# Trust_primary = (1 + f) * speed_output_fan - 1 * speed_0  + (static_pressure - ISA.P0) * area

# # Second part nozzle divergent

# gamma, static_temp = compute_nozzle_converging_pressure_ratio_phi_n(1.38, T3, 1, 0, ISA.R)

# shock = compute_nozzle_converging_pressure_ratio_prime(gamma, P3, ISA.P0)

# area, static_pressure, speed_output_fan = compute_nozzle_converging_area_mach(gamma, ISA.R, static_temp, P3, alpha, 1)

# print(area)

# Trust_sec = (alpha) * speed_output_fan - alpha  * speed_0 + static_pressure * area - ISA.P0 * area

# Trust = 28558
# m_air =  Trust/ (Trust_sec + Trust_primary) 

# print_mass_flow(m_air)


def iter_question(pres_ratio_fan):
    # Ambiant 
    T1, P1  = ambiante_condition(ISA.gamma_index, mac, ISA.T0, ISA.P0)

    # Ram recovery 

    T2, P2 = intake(RR, T1, P1)



    gamma, Cp3, T3 = compute_tot_isentropic_directly_eff_compressor(efficiency_fan, 1.4, pres_ratio_fan, T2, ISA.R)
    # norammly calcule power here 
    P3 = P2 * pres_ratio_fan
    work_fan = Cp3 *(T3 - T2)

    gamma, Cp4, T4 = compute_tot_isentropic_directly_eff_compressor(eff_bister, 1.38, boster_pres_ratio, T3, ISA.R)
    # norammly calcule power here 

    P4 = P3 * boster_pres_ratio
    work_boster = Cp4 * (T4 - T3)

    overal_prss_comp = overall_pres/boster_pres_ratio/pres_ratio_fan

    gamma, Cp3, T5 = compute_tot_isentropic_directly_eff_compressor(eff_c_s, 1.381, overal_prss_comp, T4, ISA.R)
    P5 = P4 * overal_prss_comp
    work_high = Cp3 * (T5 - T4)

    # chamber 
    P6 = (1 - combustion_chabre_loss) * P5

    T6 = TiT

    CP_cc = 1178 
    entpis_burn = 42.9 *10**6
    f = compute_f_generall(CP_cc, T6, T5, eff_chamber, entpis_burn)

    # turbine --> donc regarder au rapprot de power des  deux --> Pression high

    gamma_turbine = 1.305

    CP7 = - ISA.R * gamma_turbine /(1 - gamma_turbine)

    T7 = - work_high/((1 + f) * CP7 * eff_shaft_HP) + T6

    P7 = pressure_turbine(T6, T7, eff_press_high_turb, CP7, ISA.R, P6)


    # high turbine 

    gamma_turbine_low = 1.325
    CP8 = - ISA.R * gamma_turbine_low/(1 - gamma_turbine_low)

    T8 =  - ((1 +alpha) * work_fan + work_boster)/(eff_shaft_LP * (1 + f) * CP8) + T7

    P8 = pressure_turbine(T7, T8, eff_press_low_turb, CP8, ISA.R, P7)

    return T8, P8, f , T3, P3


iter = 0
iter_max = 100
tol = 1e-3
T8, P8, f , T3, P3 = iter_question(1.7)
start_val = 1.73
# vue que si elle augmente il diminuée regarde ou sa sera bon 
min =  start_val + iter *22
max =  start_val + 0.01 *22
# max =  start_val 

while iter < iter_max  and tol <  np.abs(P8 - P3) :
    pressure_ratio_fan = max + iter *0.001
    T8, P8, f , T3, P3 = iter_question(max + iter *0.001)
    if (P8 - P3) < 0 :
        print(iter)
        break
    print(P8 - P3, iter)
    iter +=1


# Mixer 
