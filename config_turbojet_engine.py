class turbo_jet:
    def __init__(self, delta_f, Pi, m_d_a, alpha, m_d_c_ratio, TiT, SFC_cc, SFC_ab, T, T_wet, duct_tot_press_loss, cham_tot_press_loss, mixe_tot_press_loss, eta_cc, eta_ab, eta_t):
        self.delta_f             = delta_f             # [J/kg] fuel lower heating value 
        self.Pi                  = Pi                  # [-] overall pressure ratio
        self.m_d_a               = m_d_a               # [kg/s] total air mass flow rate
        self.alpha               = alpha               # [-] bypass ratio
        self.m_d_c_ratio         = m_d_c_ratio         # [-] turbine coolant flow rate
        self.TiT                 = TiT                 # [K] turbine inlet temperature
        self.SFC_cc              = SFC_cc              # [kg/daN.h] thrust specific fuel consumption in the combustion chamber
        self.SFC_ab              = SFC_ab              # [kg/daN.h] thrust specific fuel consumption in the afterburner
        self.T                   = T                   # [lbf] thrust
        self.T_wet               = T_wet               # [lbf] thrust
        self.duct_tot_press_loss = duct_tot_press_loss # [-] total pressure loss in secondary
        self.cham_tot_press_loss = cham_tot_press_loss # [-] total combustion chamber pressure loss
        self.mixe_tot_press_loss = mixe_tot_press_loss # [-] mixing total pressure loss wrt common total pressure loss at mixer inlet (dry conditions)
        self.eta_cc              = eta_cc              # [-] combustion efficiency
        self.eta_ab              = eta_ab              # [-] combustion efficiency
        self.eta_t               = eta_t               # [-] turbine efficiency


def Tumansky_R25_300():
    mass_flow_rate                      = 56             # kg/s
    afteburner_fuel_masss_flow          = 2.5            # kg/s
    TTurbine_inlet_temperature          = 1040 + 273.15  # K
    lower_heating_value                 = 42.8 * 10**6   # J/kg
    efficiency_shafts                   = 0.995
    Ram_recovery                        = 0.98
    compressor_stage_polytropic         = 0.91
    LPC_pressure_ratio                  = 2.3
    LPT_isentropic_efficiency           = 0.93
    HPT_isentropic_effiicency           = 0.93
    Combustion_chamber_efficiency       = 0.98
    Combustoin_chamber_pressure_losses  = 0.03
    Afterburn_combustion_efficiency     = 0.91
    Afterburner_pressure_losses         = 0.06
