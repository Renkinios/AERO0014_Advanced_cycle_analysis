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
from corrected_cond import *


ratio_pressure_prim = 1.49
ratio_pressure_sec = 1.6
mass_flow_cor = 451 
alpha = 5

# ISA 35000 ft 

Mc = 0.82 
altitude = 35000

ISA = ISA_condition(altitude,True)
ISA.T0 = 218.81
ISA.P0 = 23842.3

T1, P1 = ambiante_condition(ISA.gamma_index, Mc, ISA.T0, ISA.P0)

print_stat(P1, T1, "Ambiante")




# Calcule the rapport m*/As = rho* v*
