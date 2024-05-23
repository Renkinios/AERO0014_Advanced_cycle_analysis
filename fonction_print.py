def print_stat(pressure,termo,stat) :
    '''
    Print the pressure
    Inputs :
    - pressure : Pressure
    - stat : Station number
    '''
    print("#######################",stat,"##############################")
    print("P","                                : \t",pressure/10**3, "[kPa]")
    print("T","                                : \t",termo, "[K]")

def print_trust(trust) :
    '''
    Print the trust
    Inputs :
    - trust : Trust
    '''
    print("Trust","                            : \t",trust/10**3, "[kN]")

def print_power(power) :
    '''
    Print the power
    Inputs :
    - power : Power
    '''
    print("Power","                            : \t",power/10**6, "[MW]")

def print_mass_flow(mass_flow) :
    print("Mass Flow","                        : \t",mass_flow ,"[kg/s]")

def print_speed(speed) :
    print("Speed","                            : \t",speed ,"[m/s]")

def print_area(area) :
    print("Area","                             : \t",area ,"[m^2]")

def print_mac(mac) :
    print("Mac","                              : \t",mac)

def print_SFC(SFC) :
    print("Specific fuel consumption","       : \t",SFC* 3600 * 10,"[kg/daN/h]")