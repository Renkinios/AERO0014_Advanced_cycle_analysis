def ambiante_condition(gamma, mac_number, static_temp, static_pressure) : 
    '''
    RAM effect
    Inputs : 
    - gamma : Adiabatic index
    - mac_number : Mach number
    - static_temp : Initial temperature
    tic : Initial pressure
    
    Returns :
    - T0 : Stagnation temperature
    - P0 : Stagnation pressure
    '''
    # Stagnation temperature
    T0 = static_temp * (1 + (gamma - 1) / 2 * mac_number**2)

    # Stagnation pressure
    P0 = static_pressure * (1 + (gamma - 1) / 2 * mac_number**2)**(gamma / (gamma - 1))

    return T0, P0

