
def Technical_condition(t2в_DT ,t2в_real ,k_DT ,k_real ,tk_DT ,tk_real ,delta_P_DT ,delta_P_real, pH, Элект, O2):
    # t2в_DT ВХОДНОЕ ЗНАЧЕНИЕ
    # t2в_real ВХОДНОЕ ЗНАЧЕНИЕ
    # k_DT ВХОДНОЕ ЗНАЧЕНИЕ
    # k_real ВХОДНОЕ ЗНАЧЕНИЕ
    # tk_DT ВХОДНОЕ ЗНАЧЕНИЕ
    # tk_real ВХОДНОЕ ЗНАЧЕНИЕ
    # delta_P_DT ВХОДНОЕ ЗНАЧЕНИЕ
    # delta_P_real ВХОДНОЕ ЗНАЧЕНИЕ
    # pH ВХОДНОЕ ЗНАЧЕНИЕ
    # Элект ВХОДНОЕ ЗНАЧЕНИЕ
    # O2 ВХОДНОЕ ЗНАЧЕНИЕ
    дельта_t2в = (abs(t2в_real - t2в_DT) / t2в_DT) * 100
    дельта_k = (abs(k_real - k_DT) / k_DT) * 100
    дельта_tk = (abs(tk_real - tk_DT) / tk_DT) * 100
    дельта_delta_P = (abs(delta_P_real - delta_P_DT) / delta_P_DT) * 100
    ph_max = 8.5
    ph_min = 7.5
    Элект_max = 1
    Элект_min = 0
    O2_max = 20
    O2_min = 10
    Z_ph = abs((ph_max - pH )/
                (ph_max - ((ph_max - ph_min) * 0.5) - ((pH - (ph_max - ph_min) * 0.5) / pH) * (ph_max - ph_min) * 0.5))
    Z_Элект = abs((Элект_max - Элект) / (
                Элект_max - ((Элект_max - Элект_min) * 0.5) - ((Элект - (Элект_max - Элект_min) * 0.5) / Элект) * (
                    Элект_max - Элект_min) * 0.5))
    Z_O2 = abs((O2_max - O2) / (
                O2_max - ((O2_max - O2_min) * 0.5) - ((O2 - (O2_max - O2_min) * 0.5) / O2) * (O2_max - O2_min) * 0.5))
    Z_chemical = 300 / ((1 / Z_ph) + (1 / Z_Элект) + (1 / Z_O2))
    дельта_t2в_max = 10
    дельта_t2в_min = 1.5
    дельта_k_max = 10
    дельта_k_min = 3
    дельта_tk_max = 3
    дельта_tk_min = 0.1
    дельта_delta_P_max = 20
    дельта_delta_P_min = 3

    Z_t2в = (-100 / (дельта_t2в_max - дельта_t2в_min)) * дельта_t2в + (
            (100 * дельта_t2в_max) / (дельта_t2в_max - дельта_t2в_min))
    if Z_t2в > 100:
        Z_t2в = 100
        if Z_t2в < 0:
            Z_t2в = 0
        else:
            Z_t2в = Z_t2в

    Z_дельта_k = (-100 / (дельта_k_max - дельта_k_min)) * дельта_k + (
            100 * дельта_k_max / (дельта_k_max - дельта_k_min))
    if Z_дельта_k > 100:
        Z_дельта_k = 100
        if Z_дельта_k < 0:
            Z_дельта_k = 0
        else:
            Z_дельта_k = Z_дельта_k

    Z_дельта_tk = (-100 / (дельта_tk_max - дельта_tk_min)) * дельта_tk + (
            100 * дельта_tk_max / (дельта_tk_max - дельта_tk_min))
    if Z_дельта_tk > 100:
        Z_дельта_tk = 100
        if Z_дельта_tk < 0:
            Z_дельта_tk = 0
        else:
            Z_дельта_tk = Z_дельта_tk

    Z_дельта_delta_P = (-100 / (дельта_delta_P_max - дельта_delta_P_min)) * дельта_delta_P + (
            100 * дельта_delta_P_max / (дельта_delta_P_max - дельта_delta_P_min))
    if Z_дельта_delta_P > 100:
        Z_дельта_delta_P = 100
        if Z_дельта_delta_P < 0:
            Z_дельта_delta_P = 0
        else:
            Z_дельта_delta_P = Z_дельта_delta_P

    w_t2в = 0.2
    w_дельта_k = 0.2
    w_дельта_tk = 0.1
    w_дельта_delta_P = 0.2
    w_chemical = 0.3

    ИТС = w_t2в * Z_t2в + w_дельта_k * Z_дельта_k + w_дельта_tk * Z_дельта_tk + w_дельта_delta_P * Z_дельта_delta_P + w_chemical * Z_chemical  # ВЫХОДНОЕ ЗНАЧЕНИЕ
    return ИТС  # Выходные данные
