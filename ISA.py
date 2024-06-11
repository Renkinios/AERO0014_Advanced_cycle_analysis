from basic import *


class ISA_condition : 
    def __init__(self,altitude,isa = False) : 
        # toujours verifier avec matlab 
        # alt = 9753.6

        # [T, rho, P] = atmosisa(alt);

        # % Affichage des résultats
        # fprintf('À une altitude de %.2f mètres:\n', alt);
        # fprintf('Température: %.2f K\n', T);
        # fprintf('Pression: %.2f Pa\n', P);
        # fprintf('Densité: %.4f kg/m^3\n', rho);

        # alt =

        # 9.7536e+03

        # À une altitude de 9753.60 mètres:
        # Température: 224.75 K
        # Pression: 27448.87 Pa
        # Densité: 300.5360 kg/m^3
        self.altitude = altitude
        self.R           = 287.058   # [J/kg.K] Specific gaz constant
        self.T0_r        = 288.15    # [K] Reference temperature fot C_p
        self.gamma_index = 1.4       # [-] Adiabatic index
        self.C_P         = 0         # [J/kg.K] Specific heat at constant pressure
        self.rho0        = 1.225     # [kg/m^3] Air density at sea level
        if isa : 
            T,P = atmosisa(altitude)
            self.T0 = T
            self.P0 = P
        else :
            self.T0 = 288.15
            self.P0 = 101325
        