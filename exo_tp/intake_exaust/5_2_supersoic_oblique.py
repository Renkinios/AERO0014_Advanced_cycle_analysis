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
from fonction_print import *
from cycle.ambiante_condition import *

#  A horizontal flow enters into a channel with Mach number M = 3. The lower boundary has a restriction, sloped
#  at δ = 20◦ degrees, whereas the top boundary remains horizontal. After a certain distance, the lower boundary
#  becomes horizontal again. This distance is designed such that the flow in the channel is compressed uniformly by
#  two oblique shocks, that separate three constant states (1), (2) and (3). The first shock is formed at the lower
#  restriction. A second is formed by the reflection of the first shock on the top boundary

beta_12 = 38 # degree sea chart 2 page 43 graph

M2 = 2

M3 = 1.2