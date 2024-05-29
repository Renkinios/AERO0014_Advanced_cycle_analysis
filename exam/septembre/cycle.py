from numpy import *
from scipy import interpolate
import sys
import os

# Chemin absolu du répertoire où se trouve ce script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Chemin du répertoire contenant les fichiers à importer
# parent_dir = os.path.join(current_dir, '..', '..', 'cycle')
direct_dir = os.path.join(current_dir, '..', '..')

# sys.path.append(parent_dir)
sys.path.append(direct_dir)

from findCp import *

lbToKg = 0.45359237
g=9.81
dhf = 42.8e6
TRef = 288.15
TiT = 1560
gamma = 1.4
gOverGM = gamma/(gamma-1)
gMOverG = (gamma-1)/gamma
R=287.15
Cp = gOverGM*R
Pi = 24.5 # overall pressure ratio
thrust1 = 11250 * lbToKg * g # dry thrust
thrust2 = 16860 * lbToKg * g # wet thrust
alpha = 1 # 1.23
sfc1 = alpha * 0.8/3600/10 # kg/s / N
sfc2 = alpha * 1.7/3600/10

effs_t = 0.90 ## turbine isentropic efficiencies
eff_cc = 0.99 # 0.99 ## 0.95 ## combustion efficiency
loss_cc =0.01
loss_sd =0.01
loss_mixer = 0.03 ## 0.15 ## total pressure loss in the afterburner
loss_ab =0.02

bpr = 0.3
ma = 65

M=0
TAmb = 288.15 # 258
pAmb = 101325 # 57182
 #-----------------------------------------------------------------------------
#---computemassflowrates-------------------------------------------------
#-----------------------------------------------------------------------------
mf = sfc1 * thrust1
mfAB = sfc2 * thrust2- mf
mp = ma / (1+bpr)
ms = bpr * mp
mt = mp + mf
farp = mf / mp
far = mf / (mp+ms)
farAB = (mf + mfAB)/ma

print("------------------------------------------------------------------------")
print("Mass flow rates and fuel-to-air ratios")
print("------------------------------------------------------------------------")
print("")
print("primary mass flow rate                        = %g kg/s"%(mp))
print("secondary mass flow rate                      = %g kg/s"%(mp))
print("thrust in dry conditions                      = %g N"%(thrust1))

print("fuel mass flow rate in the combustion chamber = %g kg/s"%(mf))
print("turbine mass flow rate                        = %g kg/s"%(mt))


#---allocatetableforstoringtotalconditions
p0 = zeros(9)
T0 = zeros(9)
#---farfield
p0[0] = pAmb
T0[0] = TAmb

 #-----------------------------------------------------------------------------
#---dryoperation-----------------------------------------------------------


 #-----------------------------------------------------------------------------
#---Conditionsatthecompressorinlet
T0[1] = T0[0]*(1+(gamma-1)/2*M*M)
p0[1] = pAmb*pow(T0[1]/T0[0],gamma/(gamma-1))
print("\n------------------------------------------------------------------------")
print("Combustion chamber conditions")
print("------------------------------------------------------------------------\n")
#---Compressoroutletconditionsinthecoreandefficiency

T0[4] = TiT
p0[3] = Pi * p0[1]
p0[4] = (1-loss_cc)*p0[3]
T0[3] = T0[4]
T03 = 0
Cp4r = findCp((T0[4]+TRef)/2,farp)
print("#######################")

print("mt", mt)
print("Cp4r", Cp4r)
print("mf", mf)
print("mp",mp)
print("T_ref", TRef)
print("dhf", dhf)

print("#######################")
print("The heat capacity Cp4r, at far = %g and temperature = %g is %g"%(farp,(T0[4]+TRef)/2,Cp4r))
while (abs(T0[3]- T03) > 1e-3*T0[4]):
    Cp3r = findCp((T0[3]+TRef)/2,0)
    T03 = T0[3]
    T0[3] = TRef + (mt*Cp4r*(T0[4]- TRef)- mf * eff_cc * dhf)/mp/Cp3r


print("Combustion chamber conditions p03 = %g, T03 = %g, p04 = %g, T04 = %g"%(p0[3],T0[3],p0[4],T0[4]))
print("The heat capacity Cp3r = %g"%(Cp3r))