
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
import numpy as np


alpha = 20 # bypass ratio 

p_r = 101325 
Tr = 288

M = 0.85
altitude = 10000

ISA = ISA_condition(altitude,True)
ISA.T0 = 268.34
ISA.P0 = 69681.7



T2, P2 = ambiante_condition(ISA.gamma_index, M, ISA.T0, ISA.P0)
print_stat(P2, T2, "Ambiante")

D_t = 0.8
D_h = 0.55
Nozzle_ara = np.pi *(D_t**2 - D_h**2)/4