# main.py
import numpy as np
import matplotlib.pyplot as plt
import csv
from HIDRO_VISCOSA_AT1 import resistencia_viscosa_aguas_tranquilas1
from HIDRO_VISCOSA_AT_ESCORA import resistencia_viscosa_aguas_tranquilas_escora
from HIDRO_RESIDUAL_AT import resistencia_residual_aguas_tranquilas
from HIDRO_RESIDUAL_AT_ESCORA import resistencia_residual_aguas_tranquilas_escora
from HIDRO_APENDICES_VISCOSA import resistencia_viscosa_apendices
from HIDRO_INDUCIDA import resistencia_inducida
from HIDRO_RESIDUAL_APENDICES import resistencia_residual_apendices
from HIDRO_RESIDUAL_APENDICES_ESCORA import resistencia_residual_apendices_escora

# Función principal para calcular la resistencia total
def calcular_resistencia_total(velocidad, escora, flat, Lift, Drag):
    #resultado2 = resistencia_viscosa_aguas_tranquilas1(velocidad) # NO UTILIZAMOS ESTE RESULTADO, UTILIZAMOS LA DE ESCORA
    #print("Resultado resistencia viscosa en aguas tranquilas:", resultado2, "N")

    resultado3 = resistencia_viscosa_aguas_tranquilas_escora(velocidad, escora)
    #print("Resultado resistencia viscosa en aguas tranquilas teniendo en cuenta la escora:", resultado3, "N")

    #resultado4 = resistencia_residual_aguas_tranquilas(velocidad) # NO UTILIZAMOS ESTE RESULTADO, UTILIZAMOS LA DE ESCORA
    #print("Resultado resistencia residual en aguas tranquilas:", resultado4, "N")

    resultado5 = resistencia_residual_aguas_tranquilas_escora(velocidad, escora)
    #print("Resultado resistencia residual en aguas tranquilas en función la escora:", resultado5, "N")
    
    resultado6 = resistencia_viscosa_apendices(velocidad)
    #print("Resultado resistencia viscosa de los apéndices:", resultado6, "N")

    resultado7 = resistencia_inducida(Lift, Drag, velocidad, flat, escora)
    #print("Resultado resistencia inducida de los apéndices junto con el casco es:", resultado7, "N")

    #resultado8 = resistencia_residual_apendices(velocidad) # NO UTILIZAMOS ESTE RESULTADO, UTILIZAMOS LA DE ESCORA
    #print("Resultado resistencia residual de los apéndices es:", resultado8, "N")

    #resultado9 = resistencia_residual_apendices_escora(velocidad, escora) # NO UTILIZAMOS ESTE RESULTADO, DELFT NO TRABAJA MUY BIEN AQUÍ
    #print("Resultado resistencia residual de los apéndices según la escora:", resultado9, "N")

    RESULTADO_TOTAL = resultado3 + resultado5 + resultado6 + resultado7
    #print("EL RESULTADO TOTAL DEL VALOR DE LA RESISTENCIA DEL BARCO ES:", RESULTADO_TOTAL, "N")
    return RESULTADO_TOTAL


if __name__ == "__main__":
    # Definir valores de prueba o predeterminados para ejecutar el código
    velocidades = np.linspace(0.1, 5.7, 50) # Valores entre 0.1 y 5.7 m/s
    flat = 0        # Reemplazar con el valor optimizado
    escora = 0      # Reemplazar con el valor optimizado
    Lift = 0
    Drag = 0

    resistencias = []

    for v in velocidades:
        resultado = calcular_resistencia_total(v, escora, flat, Lift, Drag)
        resistencias.append(resultado / 1000)  # Convertimos a kN

    # Guardar resultados en un archivo CSV para usar en Excel
    with open("resistencia_total.csv", mode='w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(["Velocidad (knots)", "Resistencia Total (kN)"])
        for v, r in zip(velocidades, resistencias):
            writer.writerow([v / 0.514444, r])

    # Gráfico cartesiano (opcional)
    plt.figure()
    plt.plot([v / 0.514444 for v in velocidades], resistencias, marker='o', linestyle='-', label='Resistencia Total')
    plt.xlabel("Velocidad en knots")
    plt.ylabel("Resistencia kN")
    plt.title("Resistencia Total")
    plt.grid(True)
    plt.legend()
    plt.show()
