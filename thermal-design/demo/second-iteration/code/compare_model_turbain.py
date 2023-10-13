def technical_condition_wsp(res_args, cmp_args):
    # tвых_DT Входные данные в файле с турбиной называется t_выход_цилинда_реал
    # tвых_real Входные данные
    # hвых_DT Входные данные в вайле с турбиной называется h_выход_цилинда_реал
    # hвых_real Входные данные
    # ОРР Входные данные
    # ОС Входные данные
    # Vib_h Входные данные
    # Vib_v Входные данные
    # Tem_oil Входные данные
    print(res_args)
    print(cmp_args)

    tвых_DT = res_args[2]
    hвых_DT = res_args[1]

    tвых_real = float(cmp_args[0])
    hвых_real = float(cmp_args[1])
    ОРР = float(cmp_args[2])
    ОС = float(cmp_args[3])
    Vib_h = float(cmp_args[4])
    Vib_v = float(cmp_args[5])
    Tem_oil = float(cmp_args[6])

    дельта_tвых = (abs(tвых_real - tвых_DT) / tвых_DT) * 100
    дельта_hвых = (abs(hвых_real - hвых_DT) / hвых_DT) * 100
    ОРР_max = 4.5
    ОРР_min = -1.8
    ОС_max = 0.6
    ОС_min = -0.6
    Vib_h_max = 4.5
    Vib_h_min = 0
    Vib_v_max = 4.5
    Vib_v_min = 0
    Tem_oil_max = 65.7
    Tem_oil_min = 0

    Z_ОРР = abs((ОРР_max - ОРР) / (ОРР_max - ((ОРР_max - ОРР_min) * 0.5) - ((ОРР - (ОРР_max - ОРР_min) * 0.5) / ОРР) *
                                   (ОРР_max - ОРР_min) * 0.5))
    Z_ОС = abs((ОС_max - ОС) / (
            ОС_max - ((ОС_max - ОС_min) * 0.5) - ((ОС - (ОС_max - ОС_min) * 0.5) / ОС) * (ОС_max - ОС_min) * 0.5))
    Z_Vib_h = abs((Vib_h_max - Vib_h) / (
            Vib_h_max - ((Vib_h_max - Vib_h_min) * 0.5) - ((Vib_h - (Vib_h_max - Vib_h_min) * 0.5) / Vib_h) *
            (Vib_h_max - Vib_h_min) * 0.5))
    Z_Vib_v = abs((Vib_v_max - Vib_v) / (
            Vib_v_max - ((Vib_v_max - Vib_v_min) * 0.5) - ((Vib_v - (Vib_v_max - Vib_v_min) * 0.5) / Vib_v) * (
            Vib_v_max - Vib_v_min) * 0.5))
    Z_Tem_oil = abs((Tem_oil_max - Tem_oil) / (Tem_oil_max - ((Tem_oil_max - Tem_oil_min) * 0.5) - (
            (Tem_oil - (Tem_oil_max - Tem_oil_min) * 0.5) / Tem_oil) * (Tem_oil_max - Tem_oil_min) * 0.5))
    Z_tech = 500 / ((1 / Z_ОРР) + (1 / Z_ОС) + (1 / Z_Vib_h) + (1 / Z_Vib_v) + (1 / Z_Tem_oil))
    дельта_tвых_max = 10
    дельта_tвых_min = 1
    дельта_hвых_max = 10
    дельта_hвых_min = 3

    Z_tвых = (-100 / (дельта_tвых_max - дельта_tвых_min)) * дельта_tвых + (
            (100 * дельта_tвых_max) / (дельта_tвых_max - дельта_tвых_min))
    if Z_tвых > 100:
        Z_tвых = 100
        if Z_tвых < 0:
            Z_tвых = 0
        else:
            Z_tвых = Z_tвых

    Z_hвых = (-100 / (дельта_hвых_max - дельта_hвых_min)) * дельта_hвых + (
            100 * дельта_hвых_max / (дельта_hвых_max - дельта_hвых_min))
    if Z_hвых > 100:
        Z_hвых = 100
        if Z_hвых < 0:
            Z_hвых = 0
        else:
            Z_hвых = Z_hвых

    w_tвых = 0.28
    w_hвых = 0.24
    w_tech = 0.48

    ИТС = w_tвых * Z_tвых + w_hвых * Z_hвых + w_tech * Z_tech  # ВЫХОДНОЕ ЗНАЧЕНИЕ
    verbal_assesment = ''
    recommend = ''
    state = 0
    if ИТС > 85:
        verbal_assesment = 'очень хорошее'
        recommend = 'Плановое диагностирование'
    elif 70 < ИТС < 85:
        verbal_assesment = 'хорошее'
        recommend = 'По результатам планового диагностирования'
        state = 1
    elif 50 < ИТС < 70:
        verbal_assesment = 'удовлетворительное'
        recommend = 'Усиленный контроль технического состояния, капитальный ремонт, реконструкция'
        state = 2
    elif 25 < ИТС < 50:
        verbal_assesment = 'неудовлетворительное'
        recommend = 'Дополнительное техническое обслуживание и ремонт, усиленный контроль технического состояния, техническое перевооружение'
        state = 3
    else:
        verbal_assesment = 'критическое'
        recommend = 'Вывод из эксплуатации, техническое перевооружение и реконструкция'
        state = 4

    Txt = "Технического состояния оборудования - {0} Рекомендуемое техническое воздействие - {1}ИТС равен {2:1.3f}".format(
        verbal_assesment, recommend, ИТС)
    return ИТС, verbal_assesment, recommend, state  # Выходные данные


# print(technical_condition_wsp([0, 2884, 480], [500, 2900, 2, 2, 2, 2, 50]))
