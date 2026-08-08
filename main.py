import pandas as pd
import numpy as np
from scipy.stats import poisson
import csv, os
import datetime as dt
import matplotlib.pyplot as plt

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



# -- Promedio de goles en la liga
def obtener_forma_reciente(equipo, es_local):
    
    if es_local:
        ultimos_partidos = datos_limpios[datos_limpios['HomeTeam'] == equipo]
        ultimos_partidos = ultimos_partidos.sort_values('Date', ascending=False)
        ultimos_partidos = ultimos_partidos.head(5)
        ultimos_partidos_local = ultimos_partidos['FTHG'].mean()
        ultimos_partidos_visitante = ultimos_partidos['FTAG'].mean()
        return ultimos_partidos_local, ultimos_partidos_visitante

    else:
        ultimos_partidos = datos_limpios[datos_limpios['AwayTeam'] == equipo]
        ultimos_partidos = ultimos_partidos.sort_values('Date', ascending=False)
        ultimos_partidos = ultimos_partidos.head(5)
        ultimos_partidos_local = ultimos_partidos['FTAG'].mean()
        ultimos_partidos_visitante = ultimos_partidos['FTHG'].mean()
        return ultimos_partidos_local, ultimos_partidos_visitante
        


# Funcion para sacar los porcentajes y predecir los resultados de las posibles victorias en las apuestas
def predecir_partido(escritor):
    print("\nBienvenido al Club de Analisis\n-- Equipos disponibles --\n")
    for equipo in estadisticas_equipo.index:
        print(equipo)

    print("\nEquipos para analizar\n")
    equipo_local = input("Ingresar el nombre del primer equipo\n>>> ").title()
    equipo_visitante = input("Ingresar el nombre del segundo equipo\n>>> ").title()

    if equipo_local not in estadisticas_equipo.index:
        print("Equipo inexistente")
        return
    
    if equipo_visitante not in estadisticas_equipo.index:
        print("Equipo inexistente")
        return
    
    # -- Promedio de goles anotados de Local, Visitante y en la liga
    local_promedio_goles = datos_limpios['FTHG'].mean()
    print(f"\n== Promedio de goles anotados de {equipo_local} ==\n\n{local_promedio_goles:.5f}")

    # -- Promedio de goles anotados de Visitante
    visitante_promedio_goles = datos_limpios['FTAG'].mean()
    print(f"\n== Promedio de goles anotados de {equipo_visitante} ==\n\n{visitante_promedio_goles:.5f}")


    liga_promedio_goles = (local_promedio_goles + visitante_promedio_goles) / 2
    print(f"\n== Promedio de goles en la liga ==\n\n{liga_promedio_goles:.5f}\n")

    print("="*40)

    # consulta_equipos1 = estadisticas_equipo.loc[equipo_local]
    # consulta_equipos2 = estadisticas_equipo.loc[equipo_visitante]

    goles_anotados_local, goles_recibidos_local = obtener_forma_reciente(equipo_local, True)
    print(f"\nGoles anotados el equipo local {equipo_local}: {goles_anotados_local}\n\ngoles recibidos: {goles_recibidos_local}\n")
    
    print("="*40)

    goles_anotados_visitante, goles_recibidos_visitante = obtener_forma_reciente(equipo_visitante, False)
    print(f"\nGoles anotados el equipo visitante {equipo_visitante}: {goles_anotados_visitante}\n\ngoles recibidos: {goles_recibidos_visitante}\n")

    print("="*40)

    # Calculo de la probabilidad de goles anotados por cada equipo
    lambda_local = goles_anotados_local * goles_recibidos_visitante / liga_promedio_goles
    print(f"\n== Lambda Local ==\n\n{lambda_local:.5f}")


    # Calculo de la probabilidad de goles anotados por cada equipo
    lambda_visitante = goles_anotados_visitante * goles_recibidos_local / liga_promedio_goles
    print(f"\n== Lambda Visitante ==\n\n{lambda_visitante:.5f}")

    goles_posibles = np.arange(0, 10)

    # Calculo de la probabilidad de goles anotados por cada equipo
    probabilidad_local = poisson.pmf(goles_posibles, lambda_local)
    probabilidad_visitante = poisson.pmf(goles_posibles, lambda_visitante)
    print(f"\nProbabilidad local: {probabilidad_local}\n\nProbabilidad Visitante: {probabilidad_visitante}\n")

    # -- Calculo de la matriz de probabilidades
    matriz_probabilidades = np.outer(probabilidad_local, probabilidad_visitante)
    print("================================")
    print(f"\n{equipo_local} vs {equipo_visitante}\n")
    print("================================")

    # -- Calculo de la probabilidad de victoria en Local
    probabilidad_victoria_local = np.tril(matriz_probabilidades, k=-1).sum()
    print(f"\n{equipo_local} gana: {probabilidad_victoria_local * 100:.2f}%\n")


    # -- Calculo de la probabilidad de empate
    probabilidad_empate = np.diag(matriz_probabilidades).sum()
    print(f"Empate: {probabilidad_empate * 100:.2f}%\n")


    # -- Calculo de la probabilidad de victoria de Visitante
    probabilidad_victoria_visitante = np.triu(matriz_probabilidades, k=1).sum()
    print(f"{equipo_visitante} gana: {probabilidad_victoria_visitante * 100:.2f}%\n")


    resultado = probabilidad_victoria_local + probabilidad_empate + probabilidad_victoria_visitante
    print(f"Resultado: {resultado * 100:.2f}%\n")

    over_25 = 0
    under_25 = 0
    for i in range(10):
        for j in range(10):
            if i + j >= 3:
                over_25 += matriz_probabilidades[i][j]
            else:
                under_25 += matriz_probabilidades[i][j]

    print("="*55)
    print(f"Probabilidad de más de 2.5 goles: {over_25 * 100:.2f}%")

    print("="*55)
    print(f"Probabilidad de menos de 2.5 goles: {under_25 * 100:.2f}%")
    print("="*55)

    fecha = dt.datetime.now().strftime('%Y-%m-%d')

    escritor.writerow([fecha, equipo_local, equipo_visitante, goles_anotados_local, goles_anotados_visitante, goles_recibidos_local, goles_recibidos_visitante, round(lambda_local * 100, 2), round(lambda_visitante * 100, 2), round(probabilidad_victoria_local * 100, 2), round(probabilidad_empate * 100, 2), round(probabilidad_victoria_visitante * 100, 2)])

    # Funcionalidad para saber cuantos goles pueden haber en el partido y cual podria ser el posible marcador.
    indice_maximo = np.argmax(matriz_probabilidades)
    fila, columna = np.unravel_index(indice_maximo, matriz_probabilidades.shape)
    resultado_exacto = (matriz_probabilidades[fila, columna] * 100)
    print(f"\nEl resultado más probable es\n--------------------------------\n{equipo_local}: {fila}\n{equipo_visitante}: {columna}\nResultado exacto: {resultado_exacto:.2f}%")

    # Funcionalidad para saber si ambos equipos anotaran en el mismo partido.
    ambos_equipos_anotan = 0
    ambos_equipos_no_anotan = 0

    for i in range(0, 10):
        for j in range(0, 10):
            if i >= 1 and j >= 1:
                ambos_equipos_anotan += matriz_probabilidades[i][j]
            else:
                ambos_equipos_no_anotan += matriz_probabilidades[i][j]

    print("-"*55)
    print(f"\nLa probabilidad de que ambos equipos anoten es: {ambos_equipos_anotan * 100:.2f}%")

    print("-"*55)
    print(f"La probabilidad de que ambos equipos no anoten es: {ambos_equipos_no_anotan * 100:.2f}%")
    print("-"*55)

    imagen_matriz_colorida = plt.imshow(matriz_probabilidades)
    plt.colorbar(imagen_matriz_colorida)
    goles_visitante = plt.xlabel(f"Goles del visitante: {goles_anotados_visitante}%")
    goles_local = plt.ylabel(f"Goles del local: {goles_anotados_local}%")
    plt.title(f"{equipo_local} vs {equipo_visitante}")
    plt.savefig('graficos-analisis/grafico.png')
    plt.show()



archivo_existe = os.path.exists('resultados-analisis.csv')

with open ('resultados-analisis.csv', 'a', newline='', encoding='utf-8') as archivo:
    escritor = csv.writer(archivo)

    if archivo_existe is False:
        escritor.writerow(['fecha', 'equipo_local', 'equipo_visitante', 'goles_anotados_local', 'goles_anotados_visitante', 'goles_recibidos_local', 'goles_recibidos_visitante', 'lambda_local', 'lambda_visitante', '%probabilidad_victoria_local', '%probabilidad_empate', '%probabilidad_victoria_visitante'])

    while True:

        predecir_partido(escritor)
        continuar = input("\n¿Analizar otro partido? (s/n): ").strip().lower()
        if continuar != 's':
            print("Gracias por usar el algoritmo 'Fred'")
            break
