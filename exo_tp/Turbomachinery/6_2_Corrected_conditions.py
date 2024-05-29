#  The nominal working point of an air compressor in standard conditions (pamb∗ = 1013 mbar and Tamb∗ = 15 ◦C is
#  the following:
#  • mass flow ˙m∗ = 58 kg/s
#  • rotation speed Ω∗ = 4000 rpm
#  This compressor is tested downstream of a butterfly valve which allows to vary the working point. The total pressure
#  at the inlet of the compressor is equal to p◦
#  1 = 0.55 bar and the temperature T◦
#  1 = 20◦C. The test is performed by
#  varying the mass flow rate using a second downstream valve as well as the rotation speed.
#  We assume that air is a perfect gas with γ = 1.4 and R = 287 J/kg K
#  1. Which rotation speed and flow rate in the experimental setup correspond to the nominal working point ?
#  2. What is the absorbed power with respect to the nominal conditions ?

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
RPM_sea = 4000
T1 = 293.15
P1 = 0.55 * 10**5
RPM = compute_RPM_corrected(RPM_sea, T1)
Power = compute_power_corrected(1 ,T1, P1)
