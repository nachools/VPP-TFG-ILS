import math
import VARIABLES

# Función para calcular la constante Ch
def constant():
    Ch = (-3.5837 * (VARIABLES.Tc / VARIABLES.T)) - 0.0518 * (VARIABLES.Bwl / VARIABLES.Tc) + (0.5958 * ((VARIABLES.Tc * VARIABLES.Bwl) / (VARIABLES.T * VARIABLES.Tc))) + (0.2055 * (VARIABLES.Lwl / (VARIABLES.VolC**(1/3))))
    return Ch

# Función para calcular la resistencia residual de los apéndices en función de la escora
def resistencia_residual_apendices_escora(velocidad, escora):
    Rrk = VARIABLES.VolK * VARIABLES.densidad_agua * VARIABLES.g * constant() * ((velocidad / ((VARIABLES.g * VARIABLES.Lwl)**0.5))**2) * (escora * (math.pi / 180))
    return Rrk
