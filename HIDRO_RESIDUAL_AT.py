import numpy as np
import VARIABLES
from scipy.interpolate import PchipInterpolator

# Tabla de coeficientes en función del número de Froude
coeficientes = {
    0.1: lambda: (VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (-0.0014 + ((0.0403 * VARIABLES.LCB_fpp) + (0.047 * VARIABLES.Cp) + (-0.0227 * VARIABLES.VolC**(2/3) / VARIABLES.Aw) + (-0.0119 * VARIABLES.Bwl / VARIABLES.Lwl) + (0.0061 * VARIABLES.VolC**(2/3) / VARIABLES.Sc) + (-0.0086 * VARIABLES.LCB_fpp / VARIABLES.LCF_fpp) + (-0.0307 * VARIABLES.LCB_fpp**2) + (-0.0553 * VARIABLES.Cp**2)) * VARIABLES.VolC**(1/3) / VARIABLES.Lwl),
    0.15: lambda: (VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (0.0004 + ((-0.1808 * VARIABLES.LCB_fpp) + (0.1793 * VARIABLES.Cp) + (-0.0004 * VARIABLES.VolC**(2/3) / VARIABLES.Aw) + (0.0097 * VARIABLES.Bwl / VARIABLES.Lwl) + (0.0118 * VARIABLES.VolC**(2/3) / VARIABLES.Sc) + (-0.0055 * VARIABLES.LCB_fpp / VARIABLES.LCF_fpp) + (0.1721 * VARIABLES.LCB_fpp**2) + (-0.1728 * VARIABLES.Cp**2)) * VARIABLES.VolC**(1/3) / VARIABLES.Lwl),
    0.2: lambda: (VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (0.0014 + ((-0.1071 * VARIABLES.LCB_fpp) + (0.0637 * VARIABLES.Cp) + (0.009 * VARIABLES.VolC**(2/3) / VARIABLES.Aw) + (0.0153 * VARIABLES.Bwl / VARIABLES.Lwl) + (0.0011 * VARIABLES.VolC**(2/3) / VARIABLES.Sc) + (0.0012 * VARIABLES.LCB_fpp / VARIABLES.LCF_fpp) + (0.1021 * VARIABLES.LCB_fpp**2) + (-0.0648 * VARIABLES.Cp**2)) * VARIABLES.VolC**(1/3) / VARIABLES.Lwl),
    0.25: lambda: (VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (0.0027 + ((0.0463 * VARIABLES.LCB_fpp) + (-0.1263 * VARIABLES.Cp) + (0.0150 * VARIABLES.VolC**(2/3) / VARIABLES.Aw) + (0.0274 * VARIABLES.Bwl / VARIABLES.Lwl) + (-0.0299 * VARIABLES.VolC**(2/3) / VARIABLES.Sc) + (0.0110 * VARIABLES.LCB_fpp / VARIABLES.LCF_fpp) + (-0.0595 * VARIABLES.LCB_fpp**2) + (0.1220 * VARIABLES.Cp**2)) * VARIABLES.VolC**(1/3) / VARIABLES.Lwl),
    0.3: lambda: (VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (0.0056 + ((-0.8005 * VARIABLES.LCB_fpp) + (0.4891 * VARIABLES.Cp) + (0.0269 * VARIABLES.VolC**(2/3) / VARIABLES.Aw) + (0.0519 * VARIABLES.Bwl / VARIABLES.Lwl) + (-0.0313 * VARIABLES.VolC**(2/3) / VARIABLES.Sc) + (0.0292 * VARIABLES.LCB_fpp / VARIABLES.LCF_fpp) + (0.7314 * VARIABLES.LCB_fpp**2) + (-0.3619 * VARIABLES.Cp**2)) * VARIABLES.VolC**(1/3) / VARIABLES.Lwl),
    0.35: lambda: (VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (0.0032 + ((-0.1011 * VARIABLES.LCB_fpp) + (-0.0813 * VARIABLES.Cp) + (-0.0382 * VARIABLES.VolC**(2/3) / VARIABLES.Aw) + (0.032 * VARIABLES.Bwl / VARIABLES.Lwl) + (-0.1481 * VARIABLES.VolC**(2/3) / VARIABLES.Sc) + (0.0837 * VARIABLES.LCB_fpp / VARIABLES.LCF_fpp) + (0.0223 * VARIABLES.LCB_fpp**2) + (0.1587 * VARIABLES.Cp**2)) * VARIABLES.VolC**(1/3) / VARIABLES.Lwl),
    0.4: lambda: (VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (-0.0064 + ((2.3095 * VARIABLES.LCB_fpp) + (-1.5152 * VARIABLES.Cp) + (0.0751 * VARIABLES.VolC**(2/3) / VARIABLES.Aw) + (-0.0858 * VARIABLES.Bwl / VARIABLES.Lwl) + (-0.5349 * VARIABLES.VolC**(2/3) / VARIABLES.Sc) + (0.1715 * VARIABLES.LCB_fpp / VARIABLES.LCF_fpp) + (-2.4550 * VARIABLES.LCB_fpp**2) + (1.1865 * VARIABLES.Cp**2)) * VARIABLES.VolC**(1/3) / VARIABLES.Lwl),
    0.45: lambda: (VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (-0.0171 + ((3.4017 * VARIABLES.LCB_fpp) + (-1.9862 * VARIABLES.Cp) + (0.3242 * VARIABLES.VolC**(2/3) / VARIABLES.Aw) + (-0.1450 * VARIABLES.Bwl / VARIABLES.Lwl) + (-0.8043 * VARIABLES.VolC**(2/3) / VARIABLES.Sc) + (0.2952 * VARIABLES.LCB_fpp / VARIABLES.LCF_fpp) + (-3.5284 * VARIABLES.LCB_fpp**2) + (1.3575 * VARIABLES.Cp**2)) * VARIABLES.VolC**(1/3) / VARIABLES.Lwl),
    0.5: lambda: (VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (-0.0201 + ((7.1576 * VARIABLES.LCB_fpp) + (-6.3304 * VARIABLES.Cp) + (0.5829 * VARIABLES.VolC**(2/3) / VARIABLES.Aw) + (0.1630 * VARIABLES.Bwl / VARIABLES.Lwl) + (-0.3966 * VARIABLES.VolC**(2/3) / VARIABLES.Sc) + (0.5023 * VARIABLES.LCB_fpp / VARIABLES.LCF_fpp) + (-7.1579 * VARIABLES.LCB_fpp**2) + (5.2534 * VARIABLES.Cp**2)) * VARIABLES.VolC**(1/3) / VARIABLES.Lwl),
    0.55: lambda: (VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (0.0495 + ((1.5618 * VARIABLES.LCB_fpp) + (-6.0661 * VARIABLES.Cp) + (0.8641 * VARIABLES.VolC**(2/3) / VARIABLES.Aw) + (1.1702 * VARIABLES.Bwl / VARIABLES.Lwl) + (1.7610 * VARIABLES.VolC**(2/3) / VARIABLES.Sc) + (0.9176 * VARIABLES.LCB_fpp / VARIABLES.LCF_fpp) + (-2.1191 * VARIABLES.LCB_fpp**2) + (5.4281 * VARIABLES.Cp**2)) * VARIABLES.VolC**(1/3) / VARIABLES.Lwl),
    0.6: lambda: (VARIABLES.VolC * VARIABLES.densidad_agua * VARIABLES.g) * (0.0808 + ((-5.3233 * VARIABLES.LCB_fpp) + (-1.1513 * VARIABLES.Cp) + (0.9663 * VARIABLES.VolC**(2/3) / VARIABLES.Aw) + (1.6084 * VARIABLES.Bwl / VARIABLES.Lwl) + (2.7459 * VARIABLES.VolC**(2/3) / VARIABLES.Sc) + (0.8491 * VARIABLES.LCB_fpp / VARIABLES.LCF_fpp) + (4.7129 * VARIABLES.LCB_fpp**2) + (1.1089 * VARIABLES.Cp**2)) * VARIABLES.VolC**(1/3) / VARIABLES.Lwl),
}

# Función para interpolar la resistencia residual usando PCHIP
def resistencia_residual_aguas_tranquilas(velocidad):
    numero_froude = np.array(list(coeficientes.keys()))
    resistencia_residual_calculada = np.array([coef() for coef in coeficientes.values()])
    
    # Crear el interpolador PCHIP
    pchip_interpolator = PchipInterpolator(numero_froude, resistencia_residual_calculada)
    
    # Evaluar el PCHIP en el número de Froude deseado
    Rrh = pchip_interpolator(velocidad / ((VARIABLES.g * VARIABLES.Lwl)**0.5))
    
    # Asegurarse de que el resultado no sea negativo
    Rrh = max(Rrh, 0)
    
    return Rrh
