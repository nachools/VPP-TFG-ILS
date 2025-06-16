import math 
import numpy as np
import VARIABLES
from scipy.interpolate import PchipInterpolator
from AERO_MAIN_AERO import calcular_coeficientes_y_fuerzas, interpolar_tablas, AWACe_vals, Clmax_vals, Cdpar_vals, Cdi_vals, CdTot_vals
from AERO_CALCULOS import AWAce, SailArea, ZCEdepowered, AWSce

def calcular_coeficientes_y_fuerzas(velocidad, flat, escora):
    AWACe = AWAce(velocidad, flat, escora)
    Clmax, Cdpar, Cdi, CdTot = interpolar_tablas(
        AWACe, AWACe_vals, Clmax_vals, Cdpar_vals, Cdi_vals, CdTot_vals,
        velocidad, flat, escora
    )

    Depowered_Cl = Clmax * flat
    Depowered_Cdi = Cdi * (flat ** 2)
    Depowered_Cdtot = Cdpar + Depowered_Cdi
    Depowered_ZCE = ZCEdepowered(flat)

    Lift = 0.5 * VARIABLES.densidad_aire * SailArea * Depowered_Cl * (AWSce(velocidad, flat, escora) ** 2)
    Drag = 0.5 * VARIABLES.densidad_aire * SailArea * Depowered_Cdtot * (AWSce(velocidad, flat, escora) ** 2)


    return Lift, Drag, AWACe

# Para el Solver
def calcular_Fh(Lift, Drag, velocidad, flat, escora):
    Fh = (Lift * np.cos(AWAce(velocidad, flat, escora) * np.pi / 180)) + (Drag * np.sin(AWAce(velocidad, flat, escora) * np.pi / 180))
    return Fh

def resistencia_inducida(Lift, Drag, velocidad, flat, escora):
    def calcular_coeficientes_y_fuerzas(velocidad, flat, escora):
        AWACe = AWAce(velocidad, flat, escora)
        Clmax, Cdpar, Cdi, CdTot = interpolar_tablas(
            AWACe, AWACe_vals, Clmax_vals, Cdpar_vals, Cdi_vals, CdTot_vals,
            velocidad, flat, escora
        )

        Depowered_Cl = Clmax * flat
        Depowered_Cdi = Cdi * (flat ** 2)
        Depowered_Cdtot = Cdpar + Depowered_Cdi
        Depowered_ZCE = ZCEdepowered(flat)

        Lift = 0.5 * VARIABLES.densidad_aire * SailArea * Depowered_Cl * (AWSce(velocidad, flat, escora) ** 2)
        Drag = 0.5 * VARIABLES.densidad_aire * SailArea * Depowered_Cdtot * (AWSce(velocidad, flat, escora) ** 2)


        return Lift, Drag, AWACe

    # Función para calcular la fuerza lateral producida por la escora
    def fuerza_lateral(Lift, Drag, velocidad, flat, escora):
        Fh = (Lift * np.cos(AWAce(velocidad, flat, escora) * np.pi / 180)) + (Drag * np.sin(AWAce(velocidad, flat, escora) * np.pi / 180))
        return Fh

    # Tabla de coeficientes en función del ángulo de escora
    coeficientes = {
        0: lambda: (fuerza_lateral(Lift, Drag, velocidad, flat, escora)**2) / (math.pi * 0.5 * VARIABLES.densidad_agua * (velocidad**2) * (((VARIABLES.T * ((3.7455 * (VARIABLES.Tc / VARIABLES.T)) + (-3.6246 * ((VARIABLES.Tc / VARIABLES.T)**2)) + (0.0589 * (VARIABLES.Bwl / VARIABLES.Tc)) + (-0.0296 * VARIABLES.TRk)) * (1.2306 + (-0.7256 * (velocidad / ((VARIABLES.g * VARIABLES.Lwl) ** (0.5))))))**2))),
        10: lambda: (fuerza_lateral(Lift, Drag, velocidad, flat, escora)**2) / (math.pi * 0.5 * VARIABLES.densidad_agua * (velocidad**2) * (((VARIABLES.T * ((4.4892 * (VARIABLES.Tc / VARIABLES.T)) + (-4.8454 * ((VARIABLES.Tc / VARIABLES.T)**2)) + (0.0294 * (VARIABLES.Bwl / VARIABLES.Tc)) + (-0.0176 * VARIABLES.TRk)) * (1.4231 + (-1.2971 * (velocidad / ((VARIABLES.g * VARIABLES.Lwl) ** (0.5))))))**2))),
        20: lambda: (fuerza_lateral(Lift, Drag, velocidad, flat, escora)**2) / (math.pi * 0.5 * VARIABLES.densidad_agua * (velocidad**2) * (((VARIABLES.T * ((3.9592 * (VARIABLES.Tc / VARIABLES.T)) + (-3.9804 * ((VARIABLES.Tc / VARIABLES.T)**2)) + (0.0283 * (VARIABLES.Bwl / VARIABLES.Tc)) + (-0.0075 * VARIABLES.TRk)) * (1.5450 + (-1.5622 * (velocidad / ((VARIABLES.g * VARIABLES.Lwl) ** (0.5))))))**2))),
        30: lambda: (fuerza_lateral(Lift, Drag, velocidad, flat, escora)**2) / (math.pi * 0.5 * VARIABLES.densidad_agua * (velocidad**2) * (((VARIABLES.T * ((3.4891 * (VARIABLES.Tc / VARIABLES.T)) + (-2.9577 * ((VARIABLES.Tc / VARIABLES.T)**2)) + (0.0250 * (VARIABLES.Bwl / VARIABLES.Tc)) + (-0.0272 * VARIABLES.TRk)) * (1.4744 + (-1.3499 * (velocidad / ((VARIABLES.g * VARIABLES.Lwl) ** (0.5))))))**2))),
        # Define más coeficientes según lo necesites
    }

    # Función para interpolar la resistencia inducida en función del ángulo de escora
    def resistencia_inducida1(escora):
        angulos_escora = np.array(list(coeficientes.keys()))
        resistencia_inducida_calculada = np.array([coef() for coef in coeficientes.values()])
        
        # Crear el interpolador PCHIP
        pchip_interpolator = PchipInterpolator(angulos_escora, resistencia_inducida_calculada)
        
        # Evaluar el PCHIP en el ángulo de escora deseado
        Ri = pchip_interpolator(escora)
        
        # Asegurarse de que el resultado no sea negativo
        Ri = max(Ri, 0)
        
        return Ri

    # Llamar a la función para calcular la resistencia inducida
    resistencia_inducida_calculada = resistencia_inducida1(escora)
    return resistencia_inducida_calculada

