import pandas as pd
import numpy as np

# La funcion 'read_csv' se utiliza para leer unicamente archivos 'csv' esto ayudara para que con ayuda del codigo podamos obtener toda la información necesaria para despues crear analisis deportivos.
leer_archivo = pd.read_csv("datos-partidos/premier-league1.csv")
# print(leer_archivo)

estructurar_archivo = leer_archivo.shape
# print(f"\n-- Forma del Dataset --\n{estructurar_archivo}\n")

primeras_filas = leer_archivo.head()
# print(f"-- Lectura de las primeras filas --\n{primeras_filas}\n")

columnas_tipos = leer_archivo.dtypes
# print(f"-- Columnas y tipos de datos --\n{columnas_tipos}\n")

valores_nulos = leer_archivo.isnull().sum()
# print(f"-- Se mostraran las filas y columnas con valores nulos --\n{valores_nulos}")


# -- Datos con columnas modificadas esto se hace con el fin de solo utilizar las columnas importantes para nosotros.

datos_limpios = leer_archivo[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HS', 'AS', 'HST', 'AST']].copy()
datos_limpios['Date'] = pd.to_datetime(
    datos_limpios['Date'],
    format='%d/%m/%Y'
)

print(datos_limpios)
