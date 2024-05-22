def ambiante_condition(gamma, mac_number, initial_temperature, initial_pressure) : 
    '''
    RAM effect
    Inputs : 
    - gamma : Adiabatic index
    - mac_number : Mach number
    - initial_temperature : Initial temperature
    - initial_pressure : Initial pressure
    
    Returns :
    - T0 : Stagnation temperature
    - P0 : Stagnation pressure
    '''
    # Stagnation temperature
    T0 = initial_temperature * (1 + (gamma - 1) / 2 * mac_number**2)

    # Stagnation pressure
    P0 = initial_pressure * (1 + (gamma - 1) / 2 * mac_number**2)**(gamma / (gamma - 1))

    return T0, P0

