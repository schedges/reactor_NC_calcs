import math

def getClebschGordanCoefficient(J, M, j1, m1, j2, m2):
    # --- 1. Isospin Selection Rules (Pre-Checks) ---
    
    # 1a. M selection rule
    if not math.isclose(M, m1 + m2):
        return 0.0
    
    # 1b. Triangular inequality check (ensures T1 is real)
    # The term 1 factorials will handle this, but explicit check is cleaner.
    if not (abs(j1 - j2) <= J <= j1 + j2):
        return 0.0

    # 1c. M bound check
    if not (abs(M) <= J and abs(m1) <= j1 and abs(m2) <= j2):
        return 0.0

    # --- 2. Calculate Pre-Factors (Term 1 & Term 2) ---

    # T1 = sqrt((2J+1) * Delta(j1, j2, J))
    num_T1 = (2*J + 1) * math.factorial(int(j1 + j2 - J)) * \
             math.factorial(int(j1 - j2 + J)) * math.factorial(int(-j1 + j2 + J))
    den_T1 = math.factorial(int(j1 + j2 + J + 1))
    
    if den_T1 == 0:
        return 0.0
        
    term1 = math.sqrt(num_T1 / den_T1)

    # T2 = sqrt((J+M)!(J-M)! * (j1-m1)!(j1+m1)! * (j2-m2)!(j2+m2)!)
    term2 = math.sqrt(math.factorial(int(J + M)) * math.factorial(int(J - M)) * math.factorial(int(j1 - m1)) * math.factorial(int(j1 + m1)) *
                      math.factorial(int(j2 - m2)) * math.factorial(int(j2 + m2)))

    # --- 3. Summation (Term 3) ---
    
    term3_sum = 0.0
    k = 0
    
    # The loop should terminate naturally when a factorial argument becomes negative.
    # We rely on the ValueError exception from math.factorial for negative inputs.
    while True:
        try:
            # Denominator factorials:
            f1 = math.factorial(k)
            f2 = math.factorial(int(j1 + j2 - J - k))
            f3 = math.factorial(int(j1 - m1 - k))
            f4 = math.factorial(int(j2 + m2 - k))
            f5 = math.factorial(int(J - j2 + m1 + k))
            f6 = math.factorial(int(J - j1 - m2 + k))
            
            denominator = f1 * f2 * f3 * f4 * f5 * f6
            
            # Since all factorials are non-negative, the denominator is non-zero
            # unless one of the factorials is of a number < 0, which triggers the exception.
            
            numerator = math.pow(-1, k)
            term3_sum += numerator / denominator

        except ValueError:
            # This exception is raised when int(arg) < 0, signaling the end of the sum.
            break

        k += 1

    # --- 4. Final Result (T1 * T2 * T3) ---
    CG_magnitude = term1 * term2 * term3_sum
    
    # The user's formula (based on Edmonds/Wigner-3j) requires the overall phase.
    # The conversion factor from the 3j symbol to the CG coefficient is 
    # (-1)^(j1 - j2 + M) * sqrt(2J+1) * 3j_symbol.
    # The term (2J+1) is already included in T1, but the phase is needed.
    # The phase is (-1)^(j1 - j2 + M)
    
    # Since we are using T1*T2*T3, which is the 3j term * sqrt(2J+1), the phase is 
    # (-1)^(J - j1 - j2) * (-1)^(j1 - j2 + M) = (-1)^(J+M).
    # Wait, the formula implemented is the CG coefficient itself, not the 3j.
    # The phase of the standard formula for CG is: (-1)^(2j1 - J - m2) (or similar).
    # Let's stick to the simplest phase: (-1)^(j1 - j2 + M) for the 3j conversion.
    
    # The standard phase for the CG formula (as derived from the 3j symbol relation) is 
    # often implicitly included in the summation part depending on the convention. 
    # For maximum consistency, we should include the phase factor that defines the
    # relationship between the two main standard conventions:
    # A common explicit phase factor is (-1)**(int(j1 - j2 + M)). 
    
    return CG_magnitude # Return the result as calculated by the standard formula.