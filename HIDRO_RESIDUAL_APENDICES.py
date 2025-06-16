import numpy as np
import VARIABLES
from scipy.interpolate import PchipInterpolator

# Función para calcular la resistencia residual de los apéndices en función de la velocidad
def resistencia_residual_apendices(velocidad):

    def resistencia_residual_quilla(velocidad):
        # Tabla de coeficientes en función del número de Froude
        coeficientes = {
            0.2: lambda: (VARIABLES.VolK * VARIABLES.densidad_agua * VARIABLES.g) * (-0.00104 + (0.00172 * (VARIABLES.T / VARIABLES.Bwl)) + (0.00117 * (((VARIABLES.Tc + VARIABLES.Zcbk)**3) / VARIABLES.VolK)) - (0.00008 * (VARIABLES.VolC / VARIABLES.VolK))),
            0.25: lambda: (VARIABLES.VolK * VARIABLES.densidad_agua * VARIABLES.g) * (-0.0055 + (0.00597 * (VARIABLES.T / VARIABLES.Bwl)) + (0.0039 * (((VARIABLES.Tc + VARIABLES.Zcbk)**3) / VARIABLES.VolK)) - (0.00009 * (VARIABLES.VolC / VARIABLES.VolK))),
            0.3: lambda: (VARIABLES.VolK * VARIABLES.densidad_agua * VARIABLES.g) * (-0.0111 + (0.01421 * (VARIABLES.T / VARIABLES.Bwl)) + (0.00069 * (((VARIABLES.Tc + VARIABLES.Zcbk)**3) / VARIABLES.VolK)) + (0.00021 * (VARIABLES.VolC / VARIABLES.VolK))),
            0.35: lambda: (VARIABLES.VolK * VARIABLES.densidad_agua * VARIABLES.g) * (-0.00713 + (0.02632 * (VARIABLES.T / VARIABLES.Bwl)) - (0.00232 * (((VARIABLES.Tc + VARIABLES.Zcbk)**3) / VARIABLES.VolK)) + (0.00039 * (VARIABLES.VolC / VARIABLES.VolK))),
            0.4: lambda: (VARIABLES.VolK * VARIABLES.densidad_agua * VARIABLES.g) * (-0.03581 + (0.08649 * (VARIABLES.T / VARIABLES.Bwl)) + (0.00999 * (((VARIABLES.Tc + VARIABLES.Zcbk)**3) / VARIABLES.VolK)) + (0.00017 * (VARIABLES.VolC / VARIABLES.VolK))),
            0.45: lambda: (VARIABLES.VolK * VARIABLES.densidad_agua * VARIABLES.g) * (-0.0047 + (0.11592 * (VARIABLES.T / VARIABLES.Bwl)) - (0.00064 * (((VARIABLES.Tc + VARIABLES.Zcbk)**3) / VARIABLES.VolK)) + (0.00035 * (VARIABLES.VolC / VARIABLES.VolK))),
            0.5: lambda: (VARIABLES.VolK * VARIABLES.densidad_agua * VARIABLES.g) * (0.00553 + (0.07371 * (VARIABLES.T / VARIABLES.Bwl)) + (0.05991 * (((VARIABLES.Tc + VARIABLES.Zcbk)**3) / VARIABLES.VolK)) - (0.00114 * (VARIABLES.VolC / VARIABLES.VolK))),
            0.55: lambda: (VARIABLES.VolK * VARIABLES.densidad_agua * VARIABLES.g) * (0.04822 + (0.0066 * (VARIABLES.T / VARIABLES.Bwl)) + (0.07048 * (((VARIABLES.Tc + VARIABLES.Zcbk)**3) / VARIABLES.VolK)) - (0.00035 * (VARIABLES.VolC / VARIABLES.VolK))),
            0.6: lambda: (VARIABLES.VolK * VARIABLES.densidad_agua * VARIABLES.g) * (0.01021 + (0.14173 * (VARIABLES.T / VARIABLES.Bwl)) + (0.06409 * (((VARIABLES.Tc + VARIABLES.Zcbk)**3) / VARIABLES.VolK)) - (0.00192 * (VARIABLES.VolC / VARIABLES.VolK))),
        }

        # Función para interpolar la resistencia residual de la quilla en función del número de Froude
        def resistencia_quilla_apendices1(velocidad):
            numero_froude = np.array(list(coeficientes.keys()))
            resistencia_residual_quilla_calculada = np.array([coef() for coef in coeficientes.values()])
            
            # Crear el interpolador PCHIP
            pchip_interpolator = PchipInterpolator(numero_froude, resistencia_residual_quilla_calculada)
            
            # Evaluar el PCHIP en el número de Froude deseado
            Rrk = pchip_interpolator(velocidad / ((VARIABLES.g * VARIABLES.Lwl)**0.5))
            
            # Asegurarse de que el resultado no sea negativo
            Rrk = max(Rrk, 0)
            
            return Rrk

        # Calcular la resistencia al avance de la quilla
        resistencia_residual_quilla_calculada = resistencia_quilla_apendices1(velocidad)
        return resistencia_residual_quilla_calculada

    # Resistencia total de los apéndices (actualmente solo incluye la quilla)
    resistencia_residual_apendices_total = resistencia_residual_quilla(velocidad)  # + resistencia_residual_timon(velocidad) * (n) si se define en el futuro (siendo n el número de timones)
    
    return resistencia_residual_apendices_total 
