
def establecer_variables():
    # Variables predeterminadas
    # Dimensiones del barco predeterminado medido en maxsurf
    Despl_predeterminado = 7400*9807
    Lwl_predeterminado = 11.784
    Bwl_predeterminado = 3.181
    Tc_predeterminado = 0.4
    Cm_predeterminado = 0.736
    VolC_predeterminado = 6.879
    LCB_fpp_predeterminado = 0.544 
    LCF_fpp_predeterminado = 0.575 
    Cp_predeterminado = 0.562
    Aw_predeterminado = 27.664
    T_predeterminado = 2.3
    Zcbk_predeterminado = -1.312 
    FBAV_predeterminado = 1.25 

    #Dimensiones timón, quilla y bulbo
    tk_predeterminado = 0.0514 #___
    ck_predeterminado = 0.905 
    Ak_predeterminado = 1.72 
    tr_predeterminado = 0.05 #___
    cr_predeterminado = 0.315
    Ar_predeterminado = 0.387 
    Clk_predeterminado = 0.4 
    Alatk_predeterminado = 2.0815 #ck.T
    TRk_predeterminado = 1 
    VolK_predeterminado = 0.146 #___
    Lb_predeterminado = 2.4
    Wb_predeterminado = 0.497
    Hb_predeterminado = 0.29
    Vb_predeterminado = 0.165
    WSb_predeterminado = 2.311

    #Dimensiones velas
    #Jib
    I_predeterminado = 15.8
    J_predeterminado = 4.44
    R_predeterminado = 0
    LP_predeterminado = 4.59
    HBI_predeterminado = 1.25
    #Spinnaker
    ISP_predeterminado = 15.87
    SLU_predeterminado = 17.24
    SPLentreTPL_predeterminado = 8 
    SLE_predeterminado = 15.5
    #Mainsail
    P_predeterminado = 14.95
    E_predeterminado = 5.28
    BAS_predeterminado = 1.69
    HB_predeterminado = 0.2
    MGL_predeterminado = 4.19 
    MGM_predeterminado = 3.18 
    MGU_predeterminado = 1.86 
    MGT_predeterminado = 1.02 

    #Rig
    #Mast
    Xmast_predeterminado = 5 
    MDT1_predeterminado = 0.124
    MDL1_predeterminado = 0.249
    MDT2_predeterminado = 0.124
    MDL2_predeterminado = 0.189
    Mast_length_predeterminado = 17 
    Taper_length_predeterminado = 1.2
    #Boom
    Weight_predeterminado = 40 

    # Condiciones externas 
    TWA_predeterminado = 70   # ESTO ESTA EN (º)
    TWS_predeterminado = (15) * 0.514444  # se mete la velocidad en knots el *0,514444 es para pasar a m/s

    # Otros datos necesarios
    Sc_predeterminado = (1.97 + 0.171*(Bwl_predeterminado/Tc_predeterminado))*((0.65/Cm_predeterminado)**(1/3))*((VolC_predeterminado*Lwl_predeterminado)**(1/2))
    g_predeterminada = 9.807
    densidad_agua_predeterminada = 1026
    densidad_aire_predeterminada = 1.225
    viscosidad_cinematica_predeterminada = 1.19 * 10**(-6)
    #_____________________________________________________________________________________________________________
    LPpor_predeterminado = 6.825/7.168
    SF_predeterminado = 2.15 * 7.168
    SMG_predeterminado = 0.92 * 2.15 * 7.168
    

    # Preguntar al usuario si quiere utilizar los valores predeterminados o ingresar valores nuevos
    while True:
        usar_predeterminados = input("¿Deseas utilizar los valores predeterminados? (si/no): ").lower()
        if usar_predeterminados in ['si', 'no']:
            break
        else:
            print("Por favor, responde 'si' o 'no'.")

    if usar_predeterminados == 'no':
        # Solicitar dimensiones del barco
        Despl = float(input("Ingrese el desplazamiento del barco (t): "))*9807
        Lwl = float(input("Ingrese la eslora de flotación del barco (m): "))
        Bwl = float(input("Ingrese la manga mojada del casco (m): "))
        Tc = float(input("Ingrese el calado del casco (m): "))
        Cm = float(input("Ingrese el coeficiente de la maestra: "))
        VolC = float(input("Ingrese el volumen de carena (m^3): "))
        LCB_fpp = float(input("Ingrese la fracción de eslora donde está situado la aplicación de la fuerza de empuje: "))
        LCF_fpp = float(input("Ingrese la fracción de eslora donde está situado el centro de flotación: "))
        Cp = float(input("Ingrese el coeficiente prismático: "))
        Aw = float(input("Ingrese el área de flotación a velocidad cero (m^2): "))
        T = float(input("Ingrese el calado del casco con la quilla incluida (m): "))
        Zcbk = float(input("Ingrese la posición vertical del centro de flotación de la quilla (m): "))
        FBAV = float(input("Ingrese el francobordo promedio (m): "))

        #Dimensiones timón, quilla y bulbo
        tk = float(input("Ingrese el espesor máximo del perfil de la quilla (m): "))
        ck = float(input("Ingrese la cuerda máxima del perfil de la quilla (m): "))
        Ak = float(input("Ingrese la superficie lateral de la quilla (m^2): "))
        tr = float(input("Ingrese el espesor máximo del perfil del timón (m): "))
        cr = float(input("Ingrese la cuerda máxima del perfil del timón (m): "))
        Ar = float(input("Ingrese la superficie lateral del timón (m^2): "))
        Clk = float(input("Ingrese el coeficiente de lift de la quilla: "))
        Alatk = float(input("Ingrese la superficie lateral generada por la quilla y la parte del casco que sigue a la quilla (m^2): "))
        TRk = float(input("Ingrese el valor del tupper ratio de la quilla: "))
        VolK = float(input("Ingrese el volumen de desplazamiento de la quilla (m^3): "))
        Lb = float(input("Ingrese la longitud del bulbo (m) si no tiene 0: "))
        Wb = float(input("Ingrese el ancho del bulbo (m) si no tiene 0: "))
        Hb = float(input("Ingrese la altura del bulbo (m) si no tiene 0: "))
        Vb = float(input("Ingrese el volumen del bulbo (m^3) si no tiene 0: "))
        WSb = float(input("Ingrese el área mojada del bulbo (m^2) si no tiene 0: "))

        #Dimensiones velas
        #Jib
        I = float(input("Ingrese la altura del aparejo del Jib desde la cubierta(m): "))
        J = float(input("Ingrese la distancia entre el mástil y la proa (m): "))
        R = float(input("Ingrese parámetro de forma de la baluma: "))
        LP = float(input("Ingrese la longitud perpendicular del foque desde su grátil hasta el puño de escota (m): "))
        HBI = float(input("Ingrese la distancia vertical entre la base del mástil hasta el nivel del agua (m): "))
        #Spinnaker
        ISP = float(input("Ingrese la la altura de izado del Spinnaker (m): "))
        SLU = float(input("Ingrese la longitud del grátil de spinnaker (m): "))
        SPLentreTPL = float(input("Ingrese la relación de la distancia horizontal desde la cara delantera del mástil, sin tener en cuenta los accesorios ni los rieles, medida en la línea central del barco o cerca de ella, hasta el extremo del tangón del spinnaker y la distancia vertical desde el punto mas alto de la vela mayor hasta el punto donde se encuentran las dimensiones máximas del perfil del mástil: "))
        SLE = float(input("Ingrese la longitud de la baluma del spinnaker (m): "))
        #Mainsail
        P = float(input("Ingrese la longitud del grátil de la vela mayor (m): "))
        E = float(input("Ingrese la longitud del pujamen de la vela mayor (m): "))
        BAS = float(input("Ingrese la altura de la botavara desde la cubierta (m): ")) 
        HB = float(input("Ingrese la longitud de vela mayor que hay en el puño de driza (m): "))
        MGL = float(input("Ingrese la longitud transversal de la vela mayor a una altura de 1/4 de la altura total (m): "))
        MGM = float(input("Ingrese la longitud transversal de la vela mayor a una altura de 1/2 de la altura total (m): "))
        MGU = float(input("Ingrese la longitud transversal de la vela mayor a una altura de 3/4 de la altura total (m): "))
        MGT = float(input("Ingrese la longitud transversal de la vela mayor a una altura de 7/8 de la altura total (m): "))
       
        # ___________________________ CORREGIR TEXTO DEL PRINT __________________        
        #Rig
        #Mast
        Xmast = float(input("Ingrese la posición longitudinal del mástil (m): "))
        MDT1 = float(input("Ingrese el ancho del mástil en sentido transerval a la altura de la mitad de P (m): "))
        MDL1 = float(input("Ingrese el ancho del mástil en sentido longitudinal a la altura de la mitad de P (m): "))
        MDT2 = float(input("Ingrese el ancho mínimo del mástil en sentido transerval: "))
        MDL2 = float(input("Ingrese el ancho mínimo del mástil en sentido longitudinal: "))
        Mast_length = float(input("Ingrese la altura del mástil (m): "))
        Taper_length = float(input("Ingrese la distancia vertical desde el punto mas alto de la vela mayor hasta el punto donde se encuentran las dimensiones máximas del perfil del mástil (m): "))
        #Boom
        Weight = float(input("Ingrese el peso de la botavara (kg): "))*9.807

        # Condiciones externas
        TWA = float(input("Ingrese el rumbo real del viento (º): "))
        TWS = float(input("Ingrese la velocidad del viento real (knots): "))*0.514444444 # ESTO ESTA EN (m/s)

        # Solicitar otros datos necesarios
        g = 9.807  # Valor típico (m/s^2)
        densidad_agua = 1026  # Densidad del agua en kg/m^3 (valor típico)
        densidad_aire = 1.225 # Densidad típica del aire
        viscosidad_cinematica = 1.19 * 10**(-6)  # Viscosidad cinemática (m^2/s) (valor típico)
        Sc = (1.97 + 0.171 * (Bwl / Tc)) * ((0.65 / Cm) ** (1 / 3)) * ((VolC * Lwl) ** (0.5))  # Superficie mojada sin escora a partir de los datos proporcionados
        #___________________________________________________________________________________________________________________
        LPpor = LP/J
        SF = 2.15*J
        SMG = 0.92*SF
    else:
        # Utilizar valores predeterminados
        #Dimensiones del barco predeterminado
        Despl = Despl_predeterminado
        Lwl = Lwl_predeterminado
        Bwl = Bwl_predeterminado
        Tc = Tc_predeterminado
        Cm = Cm_predeterminado
        VolC = VolC_predeterminado
        Sc = Sc_predeterminado
        LCB_fpp = LCB_fpp_predeterminado
        LCF_fpp = LCF_fpp_predeterminado
        Cp = Cp_predeterminado
        Aw = Aw_predeterminado
        T = T_predeterminado
        Zcbk = Zcbk_predeterminado
        FBAV = FBAV_predeterminado

        #Dimensiones timón, quilla y bulbo
        tk = tk_predeterminado
        ck = ck_predeterminado
        Ak = Ak_predeterminado
        tr = tr_predeterminado
        cr = cr_predeterminado
        Ar = Ar_predeterminado
        Clk = Clk_predeterminado
        Alatk = Alatk_predeterminado
        TRk = TRk_predeterminado
        VolK = VolK_predeterminado
        Lb = Lb_predeterminado
        Wb = Wb_predeterminado
        Hb = Hb_predeterminado
        Vb = Vb_predeterminado
        WSb = WSb_predeterminado

        #Dimensiones velas
        #Jib
        I = I_predeterminado
        J = J_predeterminado
        R = R_predeterminado
        LP = LP_predeterminado
        HBI = HBI_predeterminado
        #Spinnaker
        ISP = ISP_predeterminado
        SLU = SLU_predeterminado
        SPLentreTPL = SPLentreTPL_predeterminado
        SLE = SLE_predeterminado
        #Mainsail
        P = P_predeterminado
        E = E_predeterminado
        BAS = BAS_predeterminado
        HB = HB_predeterminado
        MGL = MGL_predeterminado
        MGM = MGM_predeterminado
        MGU = MGU_predeterminado
        MGT = MGT_predeterminado

        #Rig
        #Mast
        Xmast = Xmast_predeterminado
        MDT1 = MDT1_predeterminado
        MDL1 = MDL1_predeterminado
        MDT2 = MDT2_predeterminado
        MDL2 = MDL2_predeterminado
        Mast_length = Mast_length_predeterminado
        Taper_length = Taper_length_predeterminado
        #Boom
        Weight = Weight_predeterminado

        # Condiciones externas
        TWA = TWA_predeterminado
        TWS = TWS_predeterminado

        # Otros datos necesarios 
        g = g_predeterminada
        densidad_agua = densidad_agua_predeterminada
        densidad_aire = densidad_aire_predeterminada
        viscosidad_cinematica = viscosidad_cinematica_predeterminada
        Sc = (1.97 + 0.171 * (Bwl / Tc)) * ((0.65 / Cm) ** (1 / 3)) * ((VolC * Lwl) ** (0.5))  # Superficie mojada sin escora a partir de los datos proporcionados
        #_________________________________________________________________________________________________________________________________________________
        LPpor = LP/J
        SF = 2.15*J
        SMG = 0.92*SF

        #_______________________RECORDAR AÑADIR EN LA FUNCION Y EN RETURN LAS NUEVAS VARIABLES___________________________________

    return Despl, Lwl, Bwl, Tc, Cm, VolC, LCB_fpp, LCF_fpp, Cp, Aw, T, Zcbk, FBAV, tk, ck, Ak, tr, cr, Ar, Clk, Alatk, TRk, VolK, Lb, Wb, Hb, Vb, WSb, g, densidad_agua, densidad_aire, viscosidad_cinematica, Sc, I, J, R, LP, HBI, ISP, SLU, SPLentreTPL, SLE, P, E, BAS, HB, MGL, MGM, MGU, MGT, Xmast, MDT1, MDL1, MDT2, MDL2, Mast_length, Taper_length, Weight, TWA, TWS, LPpor, SF, SMG

# Llamar a la función para establecer las variables al importar el archivo
Despl, Lwl, Bwl, Tc, Cm, VolC, LCB_fpp, LCF_fpp, Cp, Aw, T, Zcbk, FBAV, tk, ck, Ak, tr, cr, Ar, Clk, Alatk, TRk, VolK, Lb, Wb, Hb, Vb, WSb, g, densidad_agua, densidad_aire, viscosidad_cinematica, Sc, I, J, R, LP, HBI, ISP, SLU, SPLentreTPL, SLE, P, E, BAS, HB, MGL, MGM, MGU, MGT, Xmast, MDT1, MDL1, MDT2, MDL2, Mast_length, Taper_length, Weight, TWA, TWS, LPpor, SF, SMG = establecer_variables()
                                                                                                                                                                                                                                                                      