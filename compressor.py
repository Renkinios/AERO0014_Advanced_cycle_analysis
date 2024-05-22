# Low Pressure Compressor (LPC)
from basic import *
from findCp import *

def compute_tot_isentropic_eff_compressor(Polytropic_eff,
                                          gamma_start,
                                          compression_factor,
                                          TiT,
                                          R,stage = 1) :
    
    compression_factor = compression_factor**stage
    tol   = 1e5
    gamma = gamma_start 
    iter  = 100 
    i     = 0 
    old_gamma = 1
    while  i < iter and abs((old_gamma -  gamma)/gamma < tol) :
        old_gamma       = gamma
        eff_iso         = eff_poly2eff_iso(compression_factor,gamma,Polytropic_eff)
        isentropic_temp = TiT * compression_factor**((gamma-1)/gamma)
        total_temp      = (isentropic_temp - TiT) / eff_iso  + TiT
        Cp              = findCp((total_temp + TiT)/2,0)
        gamma           = findGamma_indec(Cp, R)
        i += 1
    
    return gamma, Cp, total_temp

def compute_power_compressor(mass_flow, CP, TiT, ToT) :
    return mass_flow * CP *(ToT -TiT)


