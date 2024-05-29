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
from fonction_print import *
from corrected_cond import *
from cycle.compressor import *

RPM_nom = 5500
mass_flow_nom = 5.2 
compr_ratio_nom = 1.65
iso_eff_nom = 0.8
T_amb_nom = 183.15 
P1_nom = 101325
CP = 1005
R = 287.15
gamma = findGamma_indec(CP, R)

# Point at the surge ligne

# import from the graph 
ratio_p_turbine = 1.685 

P1 = P1_nom * compr_ratio_nom / ratio_p_turbine
T1 = T_amb_nom # la temperature chang epas comme une valve reste ambiant

mass_flow = compute_massFlow_by_correct(T1, P1, mass_flow_nom)

P2 = P1 * ratio_p_turbine


eff_iso =  0.84

eff_pol = eff_iso2eff_poly_compressor(ratio_p_turbine, gamma, eff_iso)

T2 = compute_temp__comb_with_poly(T1, ratio_p_turbine, eff_pol, gamma)

T2 = compute_temp_comp_iso(ratio_p_turbine, T1, gamma, eff_iso)

power = CP * (T2 -T1) * mass_flow


print_power(power)