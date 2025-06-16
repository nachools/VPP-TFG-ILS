import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator

# Función para cargar y manejar la tabla de valores desde un archivo CSV
def cargar_tabla_desde_csv(archivo_csv):
    try:
        # Leer el archivo CSV con delimitador ';'
        tabla = pd.read_csv(archivo_csv, delimiter=';', on_bad_lines='skip')
        
        # Filtrar filas con exactamente dos columnas (en caso de tener más columnas, se seleccionan las dos primeras)
        if len(tabla.columns) > 2:
            tabla = tabla.iloc[:, :2]

        # Renombrar columnas para consistencia
        tabla.columns = ['Escora', 'RM']

        # Convertir columnas a valores numéricos y eliminar filas no válidas
        tabla = tabla.apply(pd.to_numeric, errors='coerce').dropna()

        # Retornar los valores de las columnas
        return tabla['Escora'].values, tabla['RM'].values
    except Exception as e:
        print(f"Error al cargar el archivo CSV: {e}")
        return [], []

# Función para interpolar el valor de RM para un valor de escora dado
def calcular_RM(lista_escoras, lista_RM, escora):
    # Crear una función de interpolación con PCHIP usando la tabla de Escora y RM
    interpolador = PchipInterpolator(lista_escoras, lista_RM)
    RM_interpolado = interpolador(escora)
    return RM_interpolado

# Función para calcular el momento adrizante (en este ejemplo se asume que es igual a RM)
def calcular_momento_adrizante(RM_interpolado):
    momento_adrizante = RM_interpolado 
    return momento_adrizante
