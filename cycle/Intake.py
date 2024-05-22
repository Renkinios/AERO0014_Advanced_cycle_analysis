def intake(Ram_recovery_factor,T0,P0) : 
    '''
    Returns the intake parameters
    Inputs :
    - Ram_recovery_factor : Ram recovery factor
    Outputs :
    - T2 : Temperature at station 2 after Intake
    - P2 : Pressure at station 2 after Intake
    '''
    # Stagnation temperature
    T2 = T0  # Assuption that the temperature remain constant 
    # Stagnation pressure
    P2 = P0 * Ram_recovery_factor
    return T2, P2

def Ram_recovery_factor(p_2,p_1) : 
    '''
    Returns the ram recovery factor
    Inputs :
    - p_2 : Pressure at station 2
    - p_1 : Pressure at station 1
    Assumption that p_1 = p_0
    Outputs :
    - Ram_recovery_factor : Ram recovery factor
    '''
        
    return p_2/p_1