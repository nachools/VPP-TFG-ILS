import math
import numpy as np
import VARIABLES
from HIDRO_VISCOSA_AT1 import superficie_mojada
from scipy.interpolate import PchipInterpolator

# Función para calcular el número de Reynolds con comprobación de valor mínimo
def reynolds(velocidad): 
    if velocidad <= 0:
        velocidad = 1e-5  # Establece un valor mínimo positivo para evitar valores cero o negativos
    Rn = velocidad * 0.7 * (VARIABLES.Lwl / VARIABLES.viscosidad_cinematica)
    return max(Rn, 1e-5)  # Asegura que Rn sea positivo y mayor que cero

# Función para calcular el coeficiente de fricción con valor mínimo en Reynolds
def coeficiente_friccion(velocidad): 
    Rn = reynolds(velocidad)
    Cf = (0.075) / ((math.log10(Rn) - 2)**2)
    return Cf

# Tabla de coeficientes en función del ángulo de escora
coeficientes = {
    5: lambda: superficie_mojada() * (1 + (1/100) * (-4.112 + 0.054 * (VARIABLES.Bwl / VARIABLES.Tc) - 0.027 * (VARIABLES.Bwl / VARIABLES.Tc) + 6.329 * VARIABLES.Cm)),
    10: lambda: superficie_mojada() * (1 + (1/100) * (-4.522 - 0.132 * (VARIABLES.Bwl / VARIABLES.Tc) - 0.077 * (VARIABLES.Bwl / VARIABLES.Tc) + 8.738 * VARIABLES.Cm)),
    15: lambda: superficie_mojada() * (1 + (1/100) * (-3.291 - 0.389 * (VARIABLES.Bwl / VARIABLES.Tc) - 0.118 * (VARIABLES.Bwl / VARIABLES.Tc) + 8.949 * VARIABLES.Cm)),
    20: lambda: superficie_mojada() * (1 + (1/100) * (1.85 - 1.2 * (VARIABLES.Bwl / VARIABLES.Tc) - 0.109 * (VARIABLES.Bwl / VARIABLES.Tc) + 5.364 * VARIABLES.Cm)),
    25: lambda: superficie_mojada() * (1 + (1/100) * (6.51 - 2.305 * (VARIABLES.Bwl / VARIABLES.Tc) - 0.066 * (VARIABLES.Bwl / VARIABLES.Tc) + 3.443 * VARIABLES.Cm)),
    30: lambda: superficie_mojada() * (1 + (1/100) * (12.334 - 3.911 * (VARIABLES.Bwl / VARIABLES.Tc) + 0.024 * (VARIABLES.Bwl / VARIABLES.Tc) + 1.767 * VARIABLES.Cm)),
    35: lambda: superficie_mojada() * (1 + (1/100) * (14.648 - 5.182 * (VARIABLES.Bwl / VARIABLES.Tc) + 0.102 * (VARIABLES.Bwl / VARIABLES.Tc) + 3.497 * VARIABLES.Cm)),
    # Define más coeficientes según lo necesites
}

# Función para interpolar la superficie mojada en función del ángulo de escora
def interpolar_superficie_mojada(escora):
    angulos = np.array(list(coeficientes.keys()))
    superficies = np.array([coef() for coef in coeficientes.values()])
    
    # Crear el interpolador PCHIP
    pchip_interpolator = PchipInterpolator(angulos, superficies)
    
    # Evaluar el PCHIP en el ángulo de escora deseado
    Sc = pchip_interpolator(escora)
    
    return Sc

# Función para calcular la resistencia viscosa en aguas tranquilas considerando la escora
def resistencia_viscosa_aguas_tranquilas_escora(velocidad, escora):
    Scalpha = interpolar_superficie_mojada(escora)
    coefiff = coeficiente_friccion(velocidad)
    resistencia_viscosa = 0.5 * VARIABLES.densidad_agua * velocidad**2 * Scalpha * coefiff
    return resistencia_viscosa
