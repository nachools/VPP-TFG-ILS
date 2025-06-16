import math
import VARIABLES

# Función para calcular la resistencia viscosa de los apéndices
def resistencia_viscosa_apendices(velocidad):
        
    # Función para calcular la superficie mojada de la quilla
    def superficie_mojada_quilla():
        Sk = (VARIABLES.Ak * 2) + (2 * (VARIABLES.Ak / VARIABLES.ck) * VARIABLES.tk)
        return Sk

    # Función para calcular el número de Reynolds de la quilla
    def reynolds_quilla(velocidad):
        RnK = (velocidad * VARIABLES.ck) / VARIABLES.viscosidad_cinematica
        return max(RnK, 1e-5)  # Asegura un valor mínimo positivo para evitar problemas en el logaritmo

    # Función para calcular el coeficiente de fricción de la quilla mediante ITTC
    def coeficcion_friccion_quilla(velocidad):
        RnK = reynolds_quilla(velocidad)
        Cfk = 0.075 / ((math.log10(RnK) - 2)**2)
        return Cfk

    # Factor de forma (1+k) para la quilla
    def uno_mas_k():
        UMK = 1 + 2 * (VARIABLES.tk / VARIABLES.ck) + 60 * ((VARIABLES.tk / VARIABLES.ck)**4)
        return UMK

    # Función para calcular la resistencia viscosa de la quilla
    def resistencia_viscosa_quilla(velocidad):
        Rvk = uno_mas_k() * 0.5 * VARIABLES.densidad_agua * (velocidad**2) * superficie_mojada_quilla() * coeficcion_friccion_quilla(velocidad)
        return Rvk

    # Función para calcular la superficie mojada del timón
    def superficie_mojada_timon():
        Sr = (VARIABLES.Ar * 2) + (2 * (VARIABLES.Ar / VARIABLES.cr) * VARIABLES.tr)
        return Sr

    # Función para calcular el número de Reynolds del timón
    def reynolds_timon(velocidad):
        Rnr = (velocidad * VARIABLES.cr) / VARIABLES.viscosidad_cinematica
        return max(Rnr, 1e-5)  # Asegura un valor mínimo positivo para el Reynolds

    # Función para calcular el coeficiente de fricción del timón mediante ITTC
    def coeficcion_friccion_timon(velocidad):
        Rnr = reynolds_timon(velocidad)
        Cfr = 0.075 / ((math.log10(Rnr) - 2)**2)
        return Cfr

    # Factor de forma (1+k) para el timón
    def uno_mas_r():
        UMR = 1 + 2 * (VARIABLES.tr / VARIABLES.cr) + 60 * ((VARIABLES.tr / VARIABLES.cr)**4)
        return UMR

    # Función para calcular la resistencia viscosa del timón
    def resistencia_viscosa_timon(velocidad):
        Rvr = uno_mas_r() * 0.5 * VARIABLES.densidad_agua * (velocidad**2) * superficie_mojada_timon() * coeficcion_friccion_timon(velocidad)
        return Rvr
    
    def reynolds_bulbo(velocidad):
        Rnb = (velocidad * VARIABLES.Lb) / VARIABLES.viscosidad_cinematica
        return max(Rnb, 1e-5)  # Asegura un valor mínimo positivo para el Reynolds
    
    def coeficiente_friccion_bulbo(velocidad):
        Rnb = reynolds_bulbo(velocidad)
        Cfb = 0.075 / ((math.log10(Rnb) - 2)**2)
        return Cfb
    
    def Ff_bulbo():
        Ffb = 1 + 1.5*(0.5*(VARIABLES.Wb + VARIABLES.Hb)/VARIABLES.Lb)**(1.5) + 7*(0.5*(VARIABLES.Wb + VARIABLES.Hb)/VARIABLES.Lb)**(3)
        return Ffb
        
    def resistencia_viscosa_bulbo(velocidad):
        q = 0.5 * VARIABLES.densidad_agua * (velocidad**(2))
        Rvb = q * VARIABLES.WSb * coeficiente_friccion_bulbo(velocidad) * Ff_bulbo()
        return Rvb

    # Resistencia viscosa total de los apéndices
    resistencia_viscosa_total = resistencia_viscosa_quilla(velocidad)* (1) + resistencia_viscosa_bulbo(velocidad) * (1) + resistencia_viscosa_timon(velocidad) * (2) # !!!!!!!!Tiene dos timones

    return resistencia_viscosa_total
