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
        eff_iso         = eff_poly2eff_iso_compressor(compression_factor,gamma,Polytropic_eff)
        isentropic_temp = TiT * compression_factor**((gamma-1)/gamma)
        total_temp      = (isentropic_temp - TiT) / eff_iso  + TiT
        Cp              = findCp((total_temp + TiT)/2,0)
        gamma           = findGamma_indec(Cp, R)
        i += 1
    
    return gamma, Cp, total_temp

def compute_tot_isentropic_directly_eff_compressor(eff_iso,
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
        isentropic_temp = TiT * compression_factor**((gamma-1)/gamma)
        total_temp      = (isentropic_temp - TiT) / eff_iso  + TiT
        Cp              = findCp((total_temp + TiT)/2,0)
        gamma           = findGamma_indec(Cp, R)
        i += 1
    
    return gamma, Cp, total_temp

def compute_power_compressor(mass_flow, CP, TiT, ToT) :
    return mass_flow * CP *(ToT -TiT)


def Compute_press_output(factor_compress, input_press) : 
    return factor_compress * input_press

def compute_iso_compressor(pot, pit, tit ,tot, gamma) :
    pi_c = pot/pit
    ratio_t = tot/ tit
    return (pi_c**((gamma - 1)/gamma) - 1 )/( ratio_t - 1)

def eff_poly2eff_iso_compressor(pressure_ratio,gamma, poly_eff) :
    """
    Calculate the isentropic efficieny with the polytrpîc efficiency.
    
    Parameters:
    pressure_ratio (float): The pressure ratio.
    gamma (float): The adiabatic index.
    isentropic_eff (float): The isentropic efficiency.
    
    Returns:
    float: The polytropic efficiency.
    """
    return (pressure_ratio**((gamma-1)/gamma) - 1) / (pressure_ratio**((gamma-1)/(gamma * poly_eff)) - 1)

def eff_iso2eff_poly_compressor(pressure_ratio, gamma, iso_eff):
    """
    Calculer l'efficacité polytropique à partir de l'efficacité isentropique.

    Paramètres:
    pressure_ratio (float): Le rapport de pression (\(\pi_{c,A}\)).
    gamma (float): L'indice adiabatique (\(\gamma_a\)).
    iso_eff (float): L'efficacité isentropique (\(\eta_{c,s,A}\)).

    Retourne:
    float: L'efficacité polytropique (\(\eta_p\)).
    """
    term1 = np.log(pressure_ratio ** ((gamma - 1) / gamma))
    term2 = np.log((pressure_ratio ** ((gamma - 1) / gamma) - 1) / iso_eff + 1)
    return term1 / term2

def compute_power_fan(m_entrance, m_controunement, CP, TiT, ToT):
    """
    Calculer la puissance du fan.
    Args :
     - m_entrance : flow masse qui rentre dans le reacteur 
     - m_countournement : flow masse qui contourne le reacteur 
     - CP : CP lier a ce phase
     - Temperature d'input 
     - Temperature de sortie 
    """
    return (m_entrance + m_controunement ) * CP * (ToT - TiT)

def compute_m_sortant_fan(by_pass, m_entrant) : 
    return (by_pass * m_entrant)