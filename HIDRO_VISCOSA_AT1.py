import math
import VARIABLES

# Cálculo de superficie mojada
def superficie_mojada():
    Sc = (1.97 + 0.171 * (VARIABLES.Bwl / VARIABLES.Tc)) * ((0.65 / VARIABLES.Cm)**(1/3)) * ((VARIABLES.VolC * VARIABLES.Lwl)**0.5)
    return Sc

# Función para calcular la resistencia viscosa en aguas tranquilas
def resistencia_viscosa_aguas_tranquilas1(velocidad):
    # Calcular superficie mojada
    Supermo = superficie_mojada()
    
    # Cálculo número de Reynolds
    def reynolds(velocidad): 
        Rn = velocidad * 0.7 * (VARIABLES.Lwl / VARIABLES.viscosidad_cinematica)
        return max(Rn, 1e-5)  # Asegura que Rn sea positivo y mayor que cero

    # Cálculo coeficiente de fricción
    def coeficiente_friccion(velocidad): 
        Rn = reynolds(velocidad)
        Cf = (0.075) / ((math.log10(Rn) - 2)**2)
        return Cf

    # Calcular coeficiente de fricción con la velocidad dada
    coefiff = coeficiente_friccion(velocidad)

    # Calcular resistencia viscosa
    resistencia_viscosa = 0.5 * VARIABLES.densidad_agua * velocidad**2 * Supermo * coefiff
    return resistencia_viscosa
