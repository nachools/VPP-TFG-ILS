import math
import numpy as np
import VARIABLES
from HIDRO_RESIDUAL_AT import resistencia_residual_aguas_tranquilas
from scipy.interpolate import PchipInterpolator

def resistencia_residual_aguas_tranquilas_escora(velocidad, escora):
    # Verificar que el número de Froude esté en el rango requerido
    if 0.25 <= (velocidad / ((VARIABLES.g * VARIABLES.Lwl)**0.5)) <= 0.55:
        # Tabla de coeficientes para interpolar
        coeficientes = {
            0.25: lambda: ((VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (-0.0000268 - 0.0000014 * (VARIABLES.Lwl / VARIABLES.Bwl) - 0.0000057 * (VARIABLES.Bwl / VARIABLES.Tc) + 0.0000016 * ((VARIABLES.Bwl / VARIABLES.Tc)**2) - 0.000007 * VARIABLES.LCB_fpp - 0.0000017 * (VARIABLES.LCB_fpp**2))) * 6 * ((escora * (math.pi / 180))**1.7),
            0.3: lambda: ((VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (0.0006628 - 0.0000632 * (VARIABLES.Lwl / VARIABLES.Bwl) - 0.0000699 * (VARIABLES.Bwl / VARIABLES.Tc) + 0.0000069 * ((VARIABLES.Bwl / VARIABLES.Tc)**2) + 0.0000459 * VARIABLES.LCB_fpp - 0.0000004 * (VARIABLES.LCB_fpp**2))) * 6 * ((escora * (math.pi / 180))**1.7),
            0.35: lambda: ((VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (0.0016433 - 0.000214 * (VARIABLES.Lwl / VARIABLES.Bwl) - 0.000164 * (VARIABLES.Bwl / VARIABLES.Tc) + 0.0000199 * ((VARIABLES.Bwl / VARIABLES.Tc)**2) - 0.000054 * VARIABLES.LCB_fpp - 0.0000268 * (VARIABLES.LCB_fpp**2))) * 6 * ((escora * (math.pi / 180))**1.7),
            0.4: lambda: ((VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (-0.000866 - 0.0000354 * (VARIABLES.Lwl / VARIABLES.Bwl) + 0.0002226 * (VARIABLES.Bwl / VARIABLES.Tc) + 0.0000188 * ((VARIABLES.Bwl / VARIABLES.Tc)**2) - 0.00058 * VARIABLES.LCB_fpp - 0.000113 * (VARIABLES.LCB_fpp**2))) * 6 * ((escora * (math.pi / 180))**1.7),
            0.45: lambda: ((VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (-0.003273 + 0.0001372 * (VARIABLES.Lwl / VARIABLES.Bwl) + 0.0005547 * (VARIABLES.Bwl / VARIABLES.Tc) + 0.0000268 * ((VARIABLES.Bwl / VARIABLES.Tc)**2) - 0.001006 * VARIABLES.LCB_fpp - 0.000203 * (VARIABLES.LCB_fpp**2))) * 6 * ((escora * (math.pi / 180))**1.7),
            0.5: lambda: ((VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (-0.000198 - 0.000148 * (VARIABLES.Lwl / VARIABLES.Bwl) - 0.000659 * (VARIABLES.Bwl / VARIABLES.Tc) + 0.0001862 * ((VARIABLES.Bwl / VARIABLES.Tc)**2) - 0.000749 * VARIABLES.LCB_fpp - 0.000165 * (VARIABLES.LCB_fpp**2))) * 6 * ((escora * (math.pi / 180))**1.7),
            0.55: lambda: ((VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (0.0015873 - 0.000375 * (VARIABLES.Lwl / VARIABLES.Bwl) - 0.000711 * (VARIABLES.Bwl / VARIABLES.Tc) + 0.0002146 * ((VARIABLES.Bwl / VARIABLES.Tc)**2) - 0.000482 * VARIABLES.LCB_fpp - 0.000117 * (VARIABLES.LCB_fpp**2))) * 6 * ((escora * (math.pi / 180))**1.7),
        }

        # Función de interpolación para resistencia en función del número de Froude
        def resistencia_interpolada(velocidad):
            numero_froude = np.array(list(coeficientes.keys()))
            resistencia_residual_calculada = np.array([coef() for coef in coeficientes.values()])
            
            # Crear el interpolador PCHIP
            pchip_interpolator = PchipInterpolator(numero_froude, resistencia_residual_calculada)
            
            # Evaluar el PCHIP en el número de Froude deseado
            Rrh = pchip_interpolator(velocidad / ((VARIABLES.g * VARIABLES.Lwl)**0.5))
            
            return Rrh
        
        # Sumar la resistencia residual sin escora con la interpolada
        Rrht = resistencia_residual_aguas_tranquilas(velocidad) + resistencia_interpolada(velocidad)
    else:
        Rrht = resistencia_residual_aguas_tranquilas(velocidad)  # Valor cuando el número de Froude no está en el rango

    return Rrht
