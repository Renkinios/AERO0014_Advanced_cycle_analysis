from basic import *

class ISA_condition : 
    def __init__(self,altitude,isa = False) : 
        self.altitude = altitude
        self.R           = 287.51    # [J/kg.K] Specific gaz constant
        self.T0_r        = 288.15    # [K] Reference temperature fot C_p
        self.gamma_index = 1.4       # [-] Adiabatic index
        self.C_P         = 0         # [J/kg.K] Specific heat at constant pressure
        if isa : 
            T,P = atmosisa(altitude)
            self.T0 = T
            self.P0 = P
        else :
            self.T0 = 288.15
            self.P0 = 101325
        