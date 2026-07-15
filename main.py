import pandas as pd
import numpy as np
from scipy.stats import poisson

pd.set_option('display.max_columns', None)

np.set_printoptions(
    precision=3,
    suppress=True,
    linewidth=100
)


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
# Dataframe
datos_limpios = leer_archivo[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HS', 'AS', 'HST', 'AST']].copy()
datos_limpios['Date'] = pd.to_datetime(
    datos_limpios['Date'],
    format='%d/%m/%Y'
)
print(f"\n== Datos sobre los partidos ==\n\n{datos_limpios}\n")


# Estadisticas especificas sobre los partidos cuando se juega de 'Local'
estadisticas_local = datos_limpios.groupby('HomeTeam').agg(
    local_media_goles_anotados = ('FTHG', 'mean'),
    local_total_goles_anotados = ('FTHG', 'sum'),
    local_media_goles_recibidos = ('FTAG', 'mean'),
    local_total_goles_recibidos = ('FTAG', 'sum'),
    local_partidos_jugados = ('FTR', 'count')
)
print(f"\n== Estadisticas de los partidos jugados de Local ==\n\n{estadisticas_local}")


# Estadisticas especificas sobre los partidos cuando se juega de 'Visitante'
estadisticas_visitante = datos_limpios.groupby('AwayTeam').agg(
    visitante_media_goles_anotados = ('FTAG', 'mean'),
    visitante_total_goles_anotados = ('FTAG', 'sum'),
    visitante_media_goles_recibidos = ('FTHG', 'mean'),
    visitante_total_goles_recibidos = ('FTHG', 'sum'),
    visitante_partidos_jugados = ('FTR', 'count')
)
print(f"\n== Estadisticas de los partidos jugados de Visitante ==\n\n{estadisticas_visitante}")


# Las estadisticas de los partidos jugados de cada equipo siendo local y visitante se uniran en un solo dataframe.
estadisticas_equipo = estadisticas_local.join(estadisticas_visitante)
print(f"\n== Estadisticas de los partidos jugados de cada equipo siendo local y visitante ==\n\n{estadisticas_equipo}")


# -- Promedio de goles anotados de Local, Visitante y en la liga
local_promedio_goles = datos_limpios['FTHG'].mean()
print(f"\n== Promedio de goles anotados de Local ==\n\n{local_promedio_goles:.5f}")


# -- Promedio de goles anotados de Visitante
visitante_promedio_goles = datos_limpios['FTAG'].mean()
print(f"\n== Promedio de goles anotados de Visitante ==\n\n{visitante_promedio_goles:.5f}")


# -- Promedio de goles en la liga
liga_promedio_goles = (local_promedio_goles + visitante_promedio_goles) / 2
print(f"\n== Promedio de goles en la liga ==\n\n{liga_promedio_goles:.5f}")


# -- Calculo de la probabilidad de goles anotados por cada equipo
consulta_equipos1 = estadisticas_equipo.loc['Liverpool']
consulta_equipos2 = estadisticas_equipo.loc['Arsenal']


# Calculo de la probabilidad de goles anotados por cada equipo
lambda_local = consulta_equipos1['local_media_goles_anotados'] * consulta_equipos2['visitante_media_goles_recibidos'] / liga_promedio_goles
print(f"\n== Lambda Local ==\n\n{lambda_local:.5f}")


# Calculo de la probabilidad de goles anotados por cada equipo
lambda_visitante = consulta_equipos2['visitante_media_goles_anotados'] * consulta_equipos1['local_media_goles_recibidos'] / liga_promedio_goles
print(f"\n== Lambda Visitante ==\n\n{lambda_visitante:.5f}")


# -- Calculo de la probabilidad de goles anotados por cada equipo
goles_posibles = np.arange(0, 6)


# Calculo de la probabilidad de goles anotados por cada equipo
probabilidad_local = poisson.pmf(goles_posibles, lambda_local)
probabilidad_visitante = poisson.pmf(goles_posibles, lambda_visitante)
print(f"\nProbabilidad local: {probabilidad_local}\n\nProbabilidad Visitante: {probabilidad_visitante}\n")


# -- Calculo de la matriz de probabilidades
matriz_probabilidades = np.outer(probabilidad_local, probabilidad_visitante)
print(f"\n== Matriz de probabilidades ==\n\n{matriz_probabilidades}\n")


# -- Calculo de la probabilidad de victoria en Local
probabilidad_victoria_local = np.tril(matriz_probabilidades, k=-1).sum()
print(f"\n== Probabilidad de victoria en Local ==\n\n{probabilidad_victoria_local * 100:.2f}%\n")


# -- Calculo de la probabilidad de empate
probabilidad_empate = np.diag(matriz_probabilidades).sum()
print(f"\n== Probabilidad de empate ==\n\n{probabilidad_empate * 100:.2f}%\n")


# -- Calculo de la probabilidad de victoria de Visitante
probabilidad_victoria_visitante = np.triu(matriz_probabilidades, k=1).sum()
print(f"\n== Probabilidad de victoria de Visitante ==\n\n{probabilidad_victoria_visitante * 100:.2f}%\n")


resultado = probabilidad_victoria_local + probabilidad_empate + probabilidad_victoria_visitante
print(resultado)