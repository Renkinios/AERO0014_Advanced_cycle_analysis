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

