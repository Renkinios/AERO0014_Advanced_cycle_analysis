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



# An aircraft is cruising at Mach 1.75 at an altitude of 32,000 ft. Its engine is equipped with a straight intake whose
# ratio of surfaces between the throat and inlet is equal to 0.822. We assume that the air behaves as a calorically
# perfect gas with γ = 1.4 so we can use the tables in the NACA TR-1135 report [1]


#  1)
#  Consider that the intake has been designed according to proper standards. What should be the design
#  Mach number for this intake and why ?

Ar = 0.822
gamma = 1.4 

# Supersonic intakes should be designed so the shock happens at the inlet plane (i.e. the Kantrowitz limit).
# The flow is accelerate to subsonci to soncic flow in the rhorat, the MAch number behind the sohock sould 
# coresspond to the criterical area ratio

# lokking in tge table of the nasa is note  A1/ AT donc bessoin de regarder a 1/r1

alpha_nasa = 1/Ar  # if the sbock after is less important is subsonic at the troat so look in the table 
M_1_subsonic = 0.58

#  1. If the aircraft comes from low Mach condition and has not reached the Kantrowitz limit yet, the shock that is
#  normally formed in the front of the intake will still be there, upstream of the intake lips, gradually moving
#  towards the intake lips as Mach number increases to reach the Kantrowitz limit (the design Mach number).


# same thing considering here that critical at the nozzle donc subpersnonuc at the throat
M_0_supersonic = 1.55
#  2. If the aircraft is decelerating from a Mach number above the Kantrowitz limit (design Mach number), the
#  shock will be "sucked" in the intake and moved downwards the convergent. As the Mach number of 1.75 lies
#  between the isentropic limit and the Kantrowitz limit, the shock is therefore located in the convergent.
#  The choice is made coresponding to the graphe 5.4 on the course note

#  There is theoretically a third condition, corresponding to isentropic deceleration without reaching sonic conditions
#  in the throat. A shock located in the convergent will come closer to the throat for as the Mach number decreases,
#  up to the isentropic deceleration for which the shock is swallowed by the throat, with fully supersonic conditions
#  throughout the convergent and a choked nozzle. Theoretically, there is then a third condition obtained by isentropic
#  reacceleration from the isentropic conditions. The throat is then too large to decelerate the flow to sonic conditions in
#  the throat. This condition is however not practically obtainable; it would require first accelerating to the Kantrowitz
#  limit; then decelerating to obtain the isentropic conditions exactly, without unstarting the nozzle (very unlikely),
#  and then reaccelerating.

# 2)
# Assuming the engine is always exactly ingesting the mass flow passing through the throat, what are
# conditions, including potential positions of shocks.
# the possible operating condition(s) at Mach 1.75? Explain the configuration(s) and determine flow.

# ram conditions

altitude = 32000 # ft
altitude = convlength(altitude, 'ft', 'm')
print(altitude)
isa_32000 = ISA_condition(altitude, True)
isa_32000.P0 = 27448.87
isa_32000.T0 = 224.75

print_stat(isa_32000.P0, isa_32000.T0, "Static ")

Mac_number = 1.75

T1, P1 = ambiante_condition(isa_32000.gamma_index, Mac_number, isa_32000.T0, isa_32000.P0)

print_stat(P1, T1, "total")

# if the shoc happen in front of the engine 

T_shock = T1

pi_75 = 0.8346 # determine in the doc nase is correspond here to pi(M0)

P_shock = pi_75 * P1
# total pression reduce by the shock 


# Can calculate the pressure lost by the shock 
# --> mass flow max when the traot is shock loss que (m_dot - m_dot')/m_dot where m_dot is at the trhoat 
# Pour calculer sa on regarde le shock apres va crée un Mac plus faible on va regarder le rapprot d'air qui arrive 
# on prend dans les table les deux 

######################## DANGER table ############################# 
# Repesente A1 /AT always

# Shocked appen 


#  When the shock happens in the convergent, it occurs at a different Mach number Ms than the flight
#  one; downstream of the shock we will have a subsonic Mach number Ms′. We must compute Ms iteratively to find
#  equality between two ways to determine the ratio of the duct area to the throat area As/At.
#  • the Mach number upstream of the shock Ms determines the critical area ratio As/A∗. Since the mass flow
#  rate between 1 and s is the same, we can write

# As /AT = A_1 / A_t * A*/A1 * A_S /A* 
#  • we find the downstream Mach number M′
#  s. Since the throat is choked, the ratio of the area at the shock to the
#  throat As/At is equal to the critical area ratio As/A∗′, which is determined by the downstream Mach number:
#  worst case : As/At = As /a_1*
#  Starting from a supposed Mach number we compute both estimates for the area ratio As/At. If the first estimate is
#  smaller than the second, it means that the shock losses are too low, and we have to look for a higher Mach number
#  upstream of the shock. Let’s start approximately halfway the possible Mach numbers Ms = (1.75 + 1)/2 ≈ 1.4.
#  Ms As/A∗ As/At Ms′ As/At ∆As/At
