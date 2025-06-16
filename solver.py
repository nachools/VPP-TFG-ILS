import numpy as np
import csv
from scipy.optimize import minimize
import VARIABLES
import matplotlib.pyplot as plt

# Importar desde otros módulos
from AERO_MAIN_AERO import calcular_FH, calcular_FHm, calcular_FR, interpolar_tablas, AWACe_vals, Clmax_vals, Cdpar_vals, Cdi_vals, CdTot_vals
from AERO_CALCULOS import AWAce, SailArea, ZCEdepowered, AWSce
from HIDRO_MAIN_HIDRO import calcular_resistencia_total
from HIDRO_INDUCIDA import calcular_Fh
from EST_ESTABILIDAD import cargar_tabla_desde_csv, calcular_RM, calcular_momento_adrizante

from HIDRO_RESIDUAL_AT_ESCORA import resistencia_residual_aguas_tranquilas_escora
from HIDRO_VISCOSA_AT_ESCORA import resistencia_viscosa_aguas_tranquilas_escora
from HIDRO_APENDICES_VISCOSA import resistencia_viscosa_apendices
from HIDRO_INDUCIDA import resistencia_inducida
from scipy.interpolate import PchipInterpolator

# Nombre del archivo CSV de estabilidad
archivo_csv = "CURVA_RM.csv"

# Cargar tabla desde CSV
lista_escoras, valores_RM = cargar_tabla_desde_csv(archivo_csv)

# Verificar si la tabla se cargó correctamente
if len(lista_escoras) == 0 or len(valores_RM) == 0:
    raise ValueError("Error: No se pudieron cargar los datos del archivo CSV. Verifica su formato.")

def calcular_RM(lista_escoras, valores_RM, escora):
    # Crear una función de interpolación con PCHIP usando la tabla de Escora y RM
    interpolador = PchipInterpolator(lista_escoras, valores_RM)
    RM_interpolado = interpolador(escora)
    return RM_interpolado

# Función para calcular los coeficientes y fuerzas aerodinámicas
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

# Restricción de fuerzas longitudinales
def restriccion_fuerzas(variables):
    velocidad, flat, escora = variables
    Lift, Drag, _ = calcular_coeficientes_y_fuerzas(velocidad, flat, escora)
    FR = calcular_FR(Lift, Drag, velocidad, flat, escora)
    resistencia_total = calcular_resistencia_total(velocidad, escora, flat, Lift, Drag)
    EQ1 = FR - resistencia_total
    return EQ1

# Restricción de momentos
def restriccion_momentos(variables):
    velocidad, flat, escora = variables
    Lift, Drag, _ = calcular_coeficientes_y_fuerzas(velocidad, flat, escora)
    FH = calcular_FH(Lift, Drag, velocidad, flat, escora)  # Es básicamente el FH absoluto, sin el cos(theta)
    RM_interpolado = calcular_RM(lista_escoras, valores_RM, escora)
    if RM_interpolado is None:
        raise ValueError("No se pudo calcular RM. Revisa el archivo CSV o los datos de entrada.")
    momento_escorante = FH * (ZCEdepowered(flat) + VARIABLES.HBI) + calcular_Fh(Lift, Drag, velocidad, flat, escora)*(((VARIABLES.T - VARIABLES.Tc)/2) + VARIABLES.Tc)
    momento_adrizante = RM_interpolado
    EQ2 = momento_escorante - momento_adrizante
    return EQ2, RM_interpolado

# Función objetivo
def objetivo(variables):
    velocidad, _, _ = variables
    return -velocidad

# Configuración de optimización
constraints = [
    {'type': 'eq', 'fun': restriccion_fuerzas},
    {'type': 'eq', 'fun': lambda vars: restriccion_momentos(vars)[0]},
]

bounds = [(None, None), (0.4, 1), (0, 40)]
x0 = [7, 0.65, 11]  # Valor inicial

# Optimización
sol = minimize(objetivo, x0, method='SLSQP', bounds=bounds, constraints=constraints, options={'maxiter': 100, 'ftol': 1e-6})

#============================================================================================================================================
#============================================================================================================================================
# ============================================================================================================================================
# NUEVO BLOQUE: MOSTRAR RESULTADOS
#============================================================================================================================================
#============================================================================================================================================
# ============================================================================================================================================


# Nombre del archivo CSV para resultados
archivo_resultados = "resultados_optimización.csv"

# Guardar los resultados en el archivo CSV con punto y coma como separador
with open(archivo_resultados, mode='a', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    # Escribir encabezados si el archivo está vacío
    if file.tell() == 0:
        writer.writerow([
            "Estado", "Velocidad Viento (knots)", "Ángulo respecto al viento (º)", "Velocidad Óptima (knots)",
            "Flat Óptimo", "Escora Óptima (º)", "Restricción Fuerzas", "Restricción Momentos",
            "Restricción FH", "Valor RM"
        ])
    
    # Calcular las restricciones usando la solución candidata, sea exitosa o no
    r_fuerzas = restriccion_fuerzas(sol.x)
    r_momentos, RM_value = restriccion_momentos(sol.x)
    estado = "Éxito" if sol.success else "Fallo"
    
    writer.writerow([
        estado,
        VARIABLES.TWS / 0.514444,
        VARIABLES.TWA,
        -sol.fun / 0.514444,
        sol.x[1],
        sol.x[2],
        r_fuerzas,
        r_momentos,
        RM_value
    ])

# Resultados
def mostrar_resultados():
    r_fuerzas = restriccion_fuerzas(sol.x)
    r_momentos, RM_value = restriccion_momentos(sol.x)
    
    if sol.success:
        print("Optimización exitosa")
    else:
        print("La optimización no convergió. Se muestran los últimos resultados obtenidos:")
    
    print("Velocidad viento (knots): ", VARIABLES.TWS / 0.514444)
    print("Ángulo del viento (º): ", VARIABLES.TWA)
    print(f"Velocidad óptima (knots): {-sol.fun / 0.514444}")
    print(f"Flat óptimo: {sol.x[1]}")
    print(f"Escora óptima (º): {sol.x[2]}")
    print(f"Restricción Fuerzas: {r_fuerzas}")
    print(f"Restricción Momentos: {r_momentos}")
    print(f"RM: {RM_value}")
    print(f"Los resultados han sido guardados en el archivo '{archivo_resultados}'.")

mostrar_resultados()


#============================================================================================================================================
#============================================================================================================================================
# ============================================================================================================================================
# Nuevo bloque: CREACION DE TABLA completa con los valores de TWA, TWS, AWS, AWA, escora, flat,
# HullResidual, HullFriction, AppendInduced, AppendFriction, FH, FR, Fh y RM.
# ============================================================================================================================================
#============================================================================================================================================
#============================================================================================================================================

archivo_tabla_completa = "Tabla_resultados_completa.csv"

# Extraer los valores de la solución óptima
vel_opt =  sol.x[0]
flat_opt =  sol.x[1]
escora_opt =  sol.x[2]

# Calcular AWS y AWA usando las funciones importadas
aws_val = AWSce(vel_opt, flat_opt, escora_opt)
awa_val = AWAce(vel_opt, flat_opt, escora_opt)

# TWA y TWS (se convierte TWS a knots, como en la tabla de optimización)
TWA_val = VARIABLES.TWA
TWS_val = VARIABLES.TWS / 0.514444

# Calcular HullResidual (se asume igual a la resistencia total del casco)
hull_residual = resistencia_residual_aguas_tranquilas_escora(vel_opt, escora_opt)
# Para HullFriction y AppendFriction, al no disponer de funciones específicas, se asigna 0 como valor por defecto.
hull_friction = resistencia_viscosa_aguas_tranquilas_escora(vel_opt, escora_opt)
append_friction = resistencia_viscosa_apendices(vel_opt)

# Calcular Lift y Drag para obtener FH y FR
Lift, Drag, _ = calcular_coeficientes_y_fuerzas(vel_opt, flat_opt, escora_opt)
FH_val = calcular_FH(Lift, Drag, vel_opt, flat_opt, escora_opt)
FR_val = calcular_FR(Lift, Drag, vel_opt, flat_opt, escora_opt)
# Calcular AppendInduced usando la función calcular_Fh (se aplica la corrección de coseno)
append_induced = resistencia_inducida(Lift, Drag, vel_opt, flat_opt, escora_opt)

# Calcular Fh (utilizando la misma fórmula que en la restricción de fuerza inducida)
Fh_val = calcular_Fh(Lift, Drag, vel_opt, flat_opt, escora_opt) * np.cos(escora_opt * np.pi/180)

# Obtener RM (se extrae el segundo valor devuelto por la función restriccion_momentos)
RM_val = calcular_RM(lista_escoras, valores_RM, escora_opt)

# Escribir la nueva tabla en el archivo CSV
with open(archivo_tabla_completa, mode='a', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    # Escribir encabezados si el archivo está vacío
    if file.tell() == 0:
        writer.writerow([
            "Estado", "TWA", "TWS", "AWS", "AWA", "BSP", "escora", "flat",
            "HullResidual", "HullFriction", "AppendInduced", "AppendFriction",
            "FH", "FR", "Fh", "RM"
        ])
    
    writer.writerow([
        estado, 
        TWA_val,
        TWS_val,
        aws_val,
        awa_val,
        vel_opt,
        escora_opt,
        flat_opt,
        hull_residual,
        hull_friction,
        append_induced,
        append_friction,
        FH_val,
        FR_val,
        Fh_val,
        RM_val
    ])

#============================================================================================================================================
#============================================================================================================================================
# ============================================================================================================================================
# Nuevo bloque: GRAFICAR RESULTADOS
# ============================================================================================================================================
#============================================================================================================================================
#============================================================================================================================================


# ============================================================================================================================================
# NUEVO BLOQUE: MOSTRAR 1 RESULTADO
# Bucle para variar TWA de 0 a 180 grados (solo la mitad derecha) y dibujar la curva polar
# ============================================================================================================================================

TWA_vals = np.linspace(0, 180, 16)  # 16 valores entre 0 y 180 grados
vel_opt_vals = []   # Para almacenar la velocidad óptima en knots
flat_opt_vals = []
escora_opt_vals = []

for twa in TWA_vals:
    VARIABLES.TWA = twa  # Actualizar TWA en VARIABLES
    sol = minimize(objetivo, x0, method='SLSQP', bounds=bounds, constraints=constraints,
                   options={'maxiter': 100, 'ftol': 1e-6})
    if sol.success:
        vel_opt = -sol.fun / 0.514444  # Convertir de m/s a knots
        flat_opt = sol.x[1]
        escora_opt = sol.x[2]
    else:
        vel_opt = np.nan
        flat_opt = np.nan
        escora_opt = np.nan

    vel_opt_vals.append(vel_opt)
    flat_opt_vals.append(flat_opt)
    escora_opt_vals.append(escora_opt)

# Gráfico polar: se mostrará solo el rango de 0° a 180° (mitad derecha)
fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')
ax.set_theta_zero_location('N')   # 0° en la parte superior
ax.set_theta_direction(-1)          # Ángulos en sentido horario
ax.set_thetamin(0)                  # Limitar ángulo mínimo a 0°
ax.set_thetamax(180)                # Limitar ángulo máximo a 180°
ax.plot(np.deg2rad(TWA_vals), vel_opt_vals, marker='o', linestyle='-', label='Velocidad Optima (nudos)')
# Ubicar la leyenda fuera del área de dibujo
ax.legend(loc='upper left', bbox_to_anchor=(0.6, 1))
ax.set_title('Curva Polar del Barco (0° a 180°)')
# Guardar la figura como imagen
fig.savefig("grafico_polar_barco.png", dpi=300, bbox_inches='tight')
plt.show()

# Gráfico cartesiano (opcional)
plt.figure()
plt.plot(TWA_vals, vel_opt_vals, marker='o', linestyle='-', label='Velocidad Optima (nudos)')
plt.xlabel("TWA (º)")
plt.ylabel("Velocidad (nudos)")
plt.title("Curva Polar (Gráfico Cartesiano)")
plt.grid(True)
# Reposicionar la leyenda dentro del gráfico para evitar que se salga del área
plt.legend(loc='upper right')
# Guardar el gráfico cartesiano como imagen
plt.savefig("grafico_cartesiano.png", dpi=300, bbox_inches='tight')
plt.show()

# ============================================================================================================================================
# BLOQUE NUEVO: Gráfico polar para diferentes velocidades de viento (4, 6, 8, 10, 12, 14, 16, 20 y 24 knots)
# ============================================================================================================================================

# Definir las velocidades de viento en knots y convertirlas a m/s
wind_knots = np.array([6, 8, 10, 12, 14, 16, 20])  # Nuevos valores solicitados
wind_ms = wind_knots * 0.514444   # conversión a m/s

# Definir el rango de TWA para este gráfico: de 30° a 180°
TWA_vals_new = np.linspace(30, 180, 16)  # 16 puntos entre 30 y 180

# Crear el gráfico polar
fig_new = plt.figure()
ax_new = fig_new.add_subplot(111, projection='polar')
ax_new.set_theta_zero_location('N')    # 0° en la parte superior
ax_new.set_theta_direction(-1)         # sentido horario

# Opcional: limitar el rango angular (aunque se dibujen solo TWA de 0 a 180)
ax_new.set_thetamin(0)
ax_new.set_thetamax(180)

# Definir una lista de colores para las curvas (añadidos colores adicionales)
colores = ['b', 'orange', 'g', 'r', 'purple', 'brown', 'pink']

# Bucle para cada velocidad de viento
for i, tws in enumerate(wind_ms):
    vel_opt_vals_new = []  # Lista para almacenar las velocidades óptimas (en knots)
    # Bucle para cada TWA en el rango definido
    for twa in TWA_vals_new:
        VARIABLES.TWA = twa     # Actualizar TWA
        VARIABLES.TWS = tws     # Actualizar TWS (en m/s)
        sol_new = minimize(objetivo, x0, method='SLSQP', bounds=bounds,
                           constraints=constraints, options={'maxiter': 100, 'ftol': 1e-6})
        if sol_new.success:
            # Convertir la velocidad óptima de m/s a knots
            vel_opt_new = -sol_new.fun / 0.514444
        else:
            vel_opt_new = np.nan
        vel_opt_vals_new.append(vel_opt_new)
    
    # Dibujar la curva para la velocidad de viento actual con un color y leyenda
    ax_new.plot(np.deg2rad(TWA_vals_new), vel_opt_vals_new,
                linestyle='-', color=colores[i], label=f'{wind_knots[i]} nudos')

ax_new.set_title('Curva Polar (TWA: 30° a 180°) VPP')
# Ubicar la leyenda fuera del área de dibujo
ax_new.legend(loc='upper left', bbox_to_anchor=(0.9, 1.1))
# Guardar la figura como imagen
fig_new.savefig("grafico_polar_vientos.png", dpi=300, bbox_inches='tight')
plt.show()

# ============================================================================================================================================
# NUEVO BLOQUE: Gráficos polares de Escora y Flat para diferentes velocidades de viento
# ============================================================================================================================================

# Definir las velocidades de viento en knots y convertirlas a m/s (mismos valores usados anteriormente)
wind_knots = np.array([6, 8, 10, 12, 14, 16, 20])
wind_ms = wind_knots * 0.514444

# Rango de TWA para este bloque: de 30° a 180° (16 puntos)
TWA_vals_new = np.linspace(30, 180, 16)

# Listas de colores (puede reutilizar los mismos del bloque anterior o redefinir)
colores = ['b', 'orange', 'g', 'r', 'purple', 'brown', 'pink']

# --- Gráfico polar de Escora ---
fig_escora = plt.figure()
ax_escora = fig_escora.add_subplot(111, projection='polar')
ax_escora.set_theta_zero_location('N')
ax_escora.set_theta_direction(-1)
ax_escora.set_thetamin(0)
ax_escora.set_thetamax(180)

for i, tws in enumerate(wind_ms):
    escora_vals = []
    for twa in TWA_vals_new:
        VARIABLES.TWA = twa
        VARIABLES.TWS = tws
        sol_new = minimize(objetivo, x0, method='SLSQP', bounds=bounds,
                           constraints=constraints, options={'maxiter': 100, 'ftol': 1e-6})
        if sol_new.success:
            escora_vals.append(sol_new.x[2])
        else:
            escora_vals.append(np.nan)
    ax_escora.plot(np.deg2rad(TWA_vals_new), escora_vals,
                   linestyle='-', color=colores[i], label=f'{wind_knots[i]} nudos')

ax_escora.set_title('Curva Polar de Escora (TWA: 30° a 180°) VPP')
ax_escora.legend(loc='upper left', bbox_to_anchor=(0.9, 1.1))
fig_escora.savefig("grafico_polar_escora_vientos.png", dpi=300, bbox_inches='tight')
plt.show()

# --- Gráfico polar de Flat ---
fig_flat = plt.figure()
ax_flat = fig_flat.add_subplot(111, projection='polar')
ax_flat.set_theta_zero_location('N')
ax_flat.set_theta_direction(-1)
ax_flat.set_thetamin(0)
ax_flat.set_thetamax(180)

for i, tws in enumerate(wind_ms):
    flat_vals = []
    for twa in TWA_vals_new:
        VARIABLES.TWA = twa
        VARIABLES.TWS = tws
        sol_new = minimize(objetivo, x0, method='SLSQP', bounds=bounds,
                           constraints=constraints, options={'maxiter': 100, 'ftol': 1e-6})
        if sol_new.success:
            flat_vals.append(sol_new.x[1])
        else:
            flat_vals.append(np.nan)
    ax_flat.plot(np.deg2rad(TWA_vals_new), flat_vals,
                 linestyle='-', color=colores[i], label=f'{wind_knots[i]} nudos')

ax_flat.set_title('Curva Polar de Flat (TWA: 30° a 180°) VPP')
ax_flat.legend(loc='upper left', bbox_to_anchor=(0.9, 1.1))
fig_flat.savefig("grafico_polar_flat_vientos.png", dpi=300, bbox_inches='tight')
plt.show()
