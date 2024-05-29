#  The nominal operating point of an air compressor in standard conditions (pamb∗ = 1.013 bar and Tamb∗ = 288 K) is
#  defined in the following way
#  • mass flow rate : ˙m∗ = 4 kg/s
#  • pressure ratio : Πtt = p◦
#  2/p◦
#  1 = 1.5
#  • rotation speed : Ω∗ = 6000 rpm
#  • power: P∗ = 177 kW
#  This compressor is used on its nominal operating point, downstream of a resistive circuit which does not exchange
#  heat with its surroundings.

#  The air is sucked in from the atmosphere through this resistive circuit and is discharged again to the atmosphere
#  by the compressor. The atmospheric pressure is patm = 1 bar, the temperature is Tamb = 10 ◦C and the normal
#  Mach number at the outlet of the compressor is Mo = 0.3.
#  Assuming that the air can be modeled as a perfect gas with constant properties γ = 1.4 and R = 287 J/kg.K,
#  determine

#  1. the stagnation pressure at the outlet of the compressor;
#  2. the stagnation pressure at the inlet of the compressor;
#  3. the stagnation temperature at the inlet of the compressor;
#  4. the power absorbed by the compressor, its flow rate and the speed of rotation;
#  5. the area of the compressor outlet

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

ISA_sea = ISA_condition(0)
mach_number_comp = 0.3
pressure_ratio = 1.5
ISA_sea.T0 = 283.15

T2, P2 = ambiante_condition(ISA_sea.gamma_index,mach_number_comp, ISA_sea.T0, ISA_sea.P0)
print_stat(P2, T2, "ambiant condition")

P1 = P2/pressure_ratio

T_amb = 283.15
T1 = T_amb

print_stat(P1, T1, "stagnation pressure at the inlet of the compressor")
N_sea_lvl = 6000 # RPM
P_sea_lvl        = 177 # KW
mass_flow_sea_lvl = 4 # kg/s


N   = compute_RPM_corrected(N_sea_lvl, T1)
P = compute_power_corrected(P_sea_lvl, T1, P1)
mass_flow = compute_massFlow_by_correct(T1, P1, mass_flow_sea_lvl)

print("Rotasion par min : ", N, "[RPM]")
print("Puissance : ", P, "[KW]")
print("Debit massique : ", mass_flow, "[kg/s]")

# Area_comp = ? --> m_dot/(rho * v_2)
# P = ˙mCp(T_2 −T_1)
T2 = T1 + P/()





