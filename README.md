README - Programa de Predicción de Velocidad para Veleros (VPP)
=================================================================

Descripción general
-------------------
Este programa implementa un modelo de Predicción de Velocidad (VPP) para veleros en tres grados de libertad: equilibrio de fuerzas longitudinales, equilibrio de fuerzas transversales y equilibrio de momentos respecto al eje longitudinal. Todo el proceso se inicia ejecutando el archivo `solver.py`, el cual coordina los cálculos de los distintos módulos hidrodinámicos, aerodinámicos y de estabilidad para encontrar la velocidad óptima del barco para distintas condiciones de viento.

Estructura general del programa
-------------------------------
El programa está organizado de forma modular, con las siguientes carpetas/archivos principales:

- `solver.py`: archivo principal que coordina todos los cálculos, define las funciones objetivo y restricciones, ejecuta la optimización con SLSQP y genera tablas de resultados y gráficos de curvas polares.
- `VARIABLES.py`: contiene todos los parámetros geométricos y físicos del barco. El usuario puede ingresar nuevos datos o usar los valores predeterminados al iniciar la ejecución.
- Módulos aerodinámicos:
  - `AERO_MAIN_AERO.py` y `AERO_CALCULOS.py`: calculan fuerzas aerodinámicas (Lift, Drag, FH, FR) a partir del ángulo aparente del viento, depowering, y áreas vélicas.
- Módulos hidrodinámicos:
  - `HIDRO_MAIN_HIDRO.py`: calcula la resistencia total del barco sumando varias componentes.
  - `HIDRO_VISCOSA_AT_ESCORA.py`, `HIDRO_RESIDUAL_AT_ESCORA.py`, `HIDRO_INDUCIDA.py`, etc.: implementan los distintos modelos de resistencia viscosa, residual e inducida, incluyendo escora y apéndices.
- Módulo de estabilidad:
  - `EST_ESTABILIDAD.py`: carga e interpola la curva RM desde `CURVA_RM.csv` para obtener el momento adrizante en función de la escora.

Funcionamiento del solver
--------------------------
El archivo `solver.py` utiliza el método de optimización `SLSQP` para maximizar la velocidad del barco bajo dos restricciones:
1. Equilibrio de fuerzas longitudinales (FR = Resistencia total).
2. Equilibrio de momentos respecto al eje longitudinal (Momento escorante = RM).

Se optimizan tres variables:
- Velocidad del barco [m/s]
- Coeficiente de depowering de las velas (`flat`) [0.4 a 1]
- Ángulo de escora [0° a 40°]

La optimización se ejecuta para diferentes valores del ángulo verdadero del viento (TWA), y se generan:
- Archivos CSV de resultados individuales y completos.
- Gráficos de curvas polares con la velocidad máxima según el rumbo.

Entrada de datos
----------------
Al inicio del programa, se pregunta al usuario si desea usar valores predeterminados o introducir nuevos. En caso afirmativo, se solicitan:
- Parámetros del casco: desplazamiento, eslora, manga, calado, volumen, coeficientes, etc.
- Datos de apéndices: quilla, timón, bulbo.
- Parámetros vélicos: dimensiones del foque, vela mayor y spinnaker.
- Posición del mástil y botavara.
- Condiciones ambientales: TWA y TWS.

Archivos de salida
------------------
- `resultados_optimización.csv`: guarda los resultados por cada optimización de TWA.
- `Tabla_resultados_completa.csv`: incluye variables adicionales como AWS, AWA, FH, Fh, RM, etc.
- Gráficos polares de velocidad del barco en función de TWA.

Licencia
--------
El programa incluye un archivo `LICENSE` con los términos de uso definidos por el autor.

Requisitos
----------
- Python 3.x
- Bibliotecas necesarias: numpy, scipy, matplotlib, pandas

Ejemplo de ejecución
--------------------
```bash
python3 solver.py


Autores y contacto
------------------
Este programa ha sido desarrollado por:

Nombre: Ignacio López Soriano  
Email: ignacioantoniolopezsoriano@gmail.com 
Proyecto: Trabajo de Fin de Grado - Ingeniería Naval  
Universidad: Universidad Politécnica de Madrid (UPM)  
Curso: 2024-2025

Para dudas o mejoras, contactar mediante el correo proporcionado.
