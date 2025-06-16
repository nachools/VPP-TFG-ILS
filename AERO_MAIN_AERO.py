import numpy as np
from scipy.interpolate import PchipInterpolator
import VARIABLES
from AERO_CALCULOS import AWAce, AWSce, ZCEdepowered, SailArea

# Tablas de ejemplo para interpolación
AWACe_vals = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180]
Clmax_vals = [-0.52219018564236, 0.166215751453799, 0.773813859696564, 1.39134123048937, 1.46725605088546, 1.49700259341741, 1.47608251020741, 1.35773395852206, 1.21922235564551, 1.08246273065984, 0.946341525125435, 0.811144625247759, 0.68102276778865, 0.554594422058996, 0.429752220127954, 0.308394664767196, 0.193517319237071, 0.0874649801194963, -0.011471328673584, -0.106021070923083]
Cdpar_vals = [0.0599310663239225, 0.0453947532298903, 0.0341010753520315, 0.0302539954976462, 0.0445727546326417, 0.0996824502411706, 0.174068922107662, 0.247499416612346, 0.328753849545114, 0.425233992686346, 0.542039934786573, 0.680115010282305, 0.824074117734217, 0.955569726909895, 1.05952842024691, 1.13225849019972, 1.17038569439203, 1.17505351947629, 1.15528085647734, 1.12190165523735]
Cdi_vals = [0.027343124960235, 0.00536322172708703, 0.0523751145941628, 0.165252075644033, 0.183765701558454, 0.193480234764509, 0.193508032529909, 0.16984554560928, 0.142520599561454, 0.116364310531415, 0.0908485629976226, 0.0676136286884725, 0.0483966253700584, 0.0326149863114081, 0.0199064405084056, 0.0104472797280807, 0.00425127325521361, 0.000980522966640445, 0.0000661360888778923, 0.00113189284226575]
CdTot_vals = [0.0872741912841575, 0.0507579749569774, 0.0864761899461942, 0.19550607114168, 0.228338456191096, 0.293162685005679, 0.367576954637572, 0.417344962221625, 0.471274449106568, 0.541598303217762, 0.632888497784196, 0.747728638970778, 0.872470743104275, 0.988184713221304, 1.07943486075531, 1.1427057699278, 1.17463696764724, 1.17603404244293, 1.15534699256621, 1.12303354807962]

# Función para interpolar tablas
def interpolar_tablas(AWACe, AWACe_vals, Clmax_vals, Cdpar_vals, Cdi_vals, CdTot_vals, velocidad, flat, escora):
    AWACe = AWAce(velocidad, flat, escora)
    interp_func1 = PchipInterpolator(AWACe_vals, Clmax_vals)
    Clmax = interp_func1(AWACe)
    
    interp_func2 = PchipInterpolator(AWACe_vals, Cdpar_vals)
    Cdpar = interp_func2(AWACe)

    interp_func3 = PchipInterpolator(AWACe_vals, Cdi_vals)
    Cdi = interp_func3(AWACe)

    interp_func4 = PchipInterpolator(AWACe_vals, CdTot_vals)
    CdTot = interp_func4(AWACe)

    return Clmax, Cdpar, Cdi, CdTot

# Función para calcular los coeficientes depowered y las fuerzas Lift y Drag
def calcular_coeficientes_y_fuerzas(velocidad, flat, escora):
    AWACe = AWAce(velocidad, flat, escora)
    Clmax, Cdpar, Cdi, CdTot = interpolar_tablas(AWACe, AWACe_vals, Clmax_vals, Cdpar_vals, Cdi_vals, CdTot_vals, velocidad, flat, escora)

    Depowered_Cl = Clmax * flat
    Depowered_Cdi = Cdi * (flat ** 2)
    Depowered_Cdtot = Cdpar + Depowered_Cdi
    Depowered_ZCE = ZCEdepowered(flat)

    Lift = 0.5 * VARIABLES.densidad_aire * SailArea * Depowered_Cl * ((AWSce(velocidad, flat, escora))**(2))
    Drag = 0.5 * VARIABLES.densidad_aire * SailArea * Depowered_Cdtot * ((AWSce(velocidad, flat, escora))**(2))

    return Lift, Drag, AWACe


# Función para calcular FH
def calcular_FH(Lift, Drag, velocidad, flat, escora):
    FH = (Lift * np.cos(AWAce(velocidad, flat, escora) * np.pi / 180)) + (Drag * np.sin(AWAce(velocidad, flat, escora) * np.pi / 180))
    return FH

# Función para calcular FH para momentos con el cos(theta)
def calcular_FHm(Lift, Drag, velocidad, flat, escora):
    FHm = ((Lift * np.cos(AWAce(velocidad, flat, escora) * np.pi / 180)) + (Drag * np.sin(AWAce(velocidad, flat, escora) * np.pi / 180)))*np.cos(escora*np.pi/180)
    return FHm

# Función para calcular FR
def calcular_FR(Lift, Drag, velocidad, flat, escora):
    FR = (Lift * np.sin(AWAce(velocidad, flat, escora) * np.pi / 180)) - (Drag * np.cos(AWAce(velocidad, flat, escora) * np.pi / 180))
    return FR
