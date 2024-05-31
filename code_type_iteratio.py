def trust_7_3(iter,v_0):
    m_flow = compute_massFlow_correct2massFlow(T1, P1, m_dot_np[iter]) 
    P2     = P1 * interpol_fan(m_dot_np[iter])
    gamma, Cp, T2 = compute_tot_isentropic_directly_eff_compressor(interpol_eta_s(m_dot_np[iter]), 1.38, interpol_fan(m_dot_np[iter]), T1, ISA.R)
    # print("T2: ", T2)
    v_j, _, Cp, mach_number, static_temp = compute_mach_exhaust(P2, ISA.P0, gamma, T2, 0, m_dot_np[iter], ISA.R)
    # print("v_j: ", v_j)
    Trust_approx = m_flow *(v_j - v_0)
    return Trust_approx

min_arg, max_arg = 0, len(m_dot_np) - 1
while iter < iter_max  and min_arg <= max_arg:
    # m_flow = (compute_massFlow_correct2massFlow(T1, P1, m_dot_np[iter]) + compute_massFlow_correct2massFlow(T1, P1, m_dot_np[len(m_dot_np)-1]))/2
    # P2     = P1 * interpol_fan(m_dot_np[iter])
    # gamma, Cp, T2 = compute_tot_isentropic_directly_eff_compressor(interpol_eta_s(m_dot_np[iter]), 1.38, interpol_fan(m_dot_np[iter]), T1, ISA.R)
    # # print("T2: ", T2)
    # v_j, gamma, Cp, mach_number, static_temp = compute_mach_exhaust(P2, ISA.P0, gamma, T2, 0, m_dot_np[iter], ISA.R)
    # # print("v_j: ", v_j)
    # Trust_approx = m_flow *(v_j - v_0)
    mid_arg =  (min_arg + max_arg) // 2
    Trust_approx_min = trust_7_3(min_arg,v_0)
    Trust_approx_max = trust_7_3(max_arg,v_0)
    Trust_approx_mid = trust_7_3(mid_arg,v_0)
    if min_arg == max_arg:
        break
    if abs(Trust_approx_mid - true_Trust) < tol:
        break
    if np.abs(true_Trust - Trust_approx_min) < np.abs(true_Trust - Trust_approx_max) : 
        max_arg = mid_arg
    else :
        min_arg = mid_arg
    
    iter += 1
    
print("iter: ", iter)
print("Trust_approx_mid: ", Trust_approx_mid)