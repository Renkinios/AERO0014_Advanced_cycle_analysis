
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
from cycle.comb_chamber import *
from basic import *

MAc =compute_fuse_cond_shock_iter(110 * 10**5, 3300, 1.33,45.1, 1)

p2 = Total_pression2static_pression(1.33, 110 * 10**5,5.2033)
print("P2",p2)
t_2 = Total_temp2static_temp(1.33, 3300, 5.2033)
print("T2",t_2)