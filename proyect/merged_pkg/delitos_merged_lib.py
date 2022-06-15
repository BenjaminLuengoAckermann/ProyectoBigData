import sys
import os
from typing import Dict

from sqlalchemy import column
# Configuracion de Carpetas
ABSOLUTE_PATH = os.path.abspath(__file__)
FILE_DIRECTORY = os.path.dirname(ABSOLUTE_PATH)
PARENT_DIRECTORY = os.path.dirname(FILE_DIRECTORY)
sys.path.insert(0, PARENT_DIRECTORY)

import itertools
from cmath import nan
import pandas as pd
import numpy as np
import fuzzywuzzy
from fuzzywuzzy import process
import common_libs.cleaning_module as cm
import common_libs.calculos_delitos as calculos
import common_libs.utils as utilidades
import common_libs.mapas as plot_map
import common_libs.franja_horaria as franja
import common_libs.graficador as graficador
import matplotlib.pyplot as plt
import merged_pkg.establecimientos_educativos as establecimientos
import merged_pkg.locales_bailables as locales_bailables
import merged_pkg.subtes as subtes


def ejecutar(ruta):
    # read in all our data
    delitos = pd.read_csv(ruta, index_col=False) 
    # Podriamos especificar un index_col=0 para que el id_mapa sea el indice de nuestra set.

    # set seed for reproducibility
    np.random.seed(0) 
    print("Longitud delitos: ", delitos.shape)
    # Muestra las primeras 5 filas
    print(delitos.head())

    # get the number of missing data points per column
    missing_values_count = delitos.isnull().sum()

    # cantidad total de valores faltantes
    total_cells = np.product(delitos.shape)
    total_missing = missing_values_count.sum()

    # procentaje de data que falta
    percent_missing = (total_missing/total_cells) * 100
    print("\nCantidad de datos faltantes: ", total_missing)
    print("\nPorcentaje de datos faltantes: ", percent_missing)

    # get all the unique values in the 'barrio' column
    barrios = delitos['barrio'].unique()

    # sort them alphabetically and then take a closer look
    #barrios.sort()
    """print("\n ---- Barrios ---- {}\n".format(len(barrios)))

    for barrio in barrios:
        print(barrio)""" 


    delitos = cm.limpiar(df=delitos, column="barrio")

    # get the top 10 closest matches to "south korea"
    matches = fuzzywuzzy.process.extract("boca", barrios, limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)
    # take a look at them
    """print("Matches", matches)"""
    cm.replace_matches_in_column(df=delitos, column="barrio", string_to_match="boca", min_ratio=72)

    
    # Graficar y calcular tendencias respecto a delitos en invierno por año y franja
    """ graficar_four_trends(df=delitos, agrupadores=["anio", "estacion", "franja_horaria"], 
                            lista_objetivo_trends=["Invierno"],
                            titulo_print="Tendencia de Delitos por Invierno para cada año")

      # Distribucion de horarios de robos en invierno y verano
    graficar_two_trends(df=delitos, agrupadores=["franja_horaria", "estacion"],
                             lista_objetivo_trends=["Verano", "Invierno"],
                             titulo_print="Tendencia de Delitos por Horarios para cada Estacion")"""
    
    
    
    # get all the unique values in the 'Barrio' column
    barrios = delitos['barrio'].unique()
    lista_barrios = []
    for barrio in barrios:
        lista_barrios.append(delitos.loc[delitos.barrio == barrio])

    print("\n\t -------- Cantidad de delitos por barrio -------- \n")

    acum, index_max, max, dictio = calculos.calcular_cantidad_delitos_por_columna(lista=lista_barrios, columna=barrios, 
    mensaje="Cantidad de delitos en barrio ")

    total_delitos = delitos.barrio.shape[0]
    print("\nCantidad total de delitos: {} y la suma de delitos por barrio es: {}".format(total_delitos, acum))
    print("\nEl barrio con mas delitos {} con {} delitos".format(barrios[index_max].upper(),
                                                            max))
   
    """ graficador.graficar_pie(diccionario=dictio, column_name="delitos", titulo_grafico="Grafico de Delitos por Barrio")
    dictio_barrios_ordenado = utilidades.sort_dict_by_values(dictionary=dictio, desc=True)
    dictio_establecimientos_ordenado = establecimientos.ejecutar()
    establecimientos.relacion_establecimientos_delito(dict_delitos=dictio_barrios_ordenado,
                                        dict_establecimientos=dictio_establecimientos_ordenado)
    """
    dictio_locales_ordenado, df_locales = locales_bailables.ejecutar()
    # Graficamos Tree Map para Delitos y Locales Bailables (los 7 que mas tienen)
    """ graficador.graficar_tree_map(diccionario=dict(itertools.islice(dictio_locales_ordenado.items(), 7)), 
                                column_name="delitos", 
                                titulo_grafico="Gráfico de los 7 Barrios con más Locales Bailables")
    graficador.graficar_tree_map(diccionario=dict(itertools.islice(dictio_barrios_ordenado.items(), 7)), 
                                column_name="delitos",                                 
                                 titulo_grafico="Gráfico de los 7 Barrios con más Delitos")
    locales_bailables.relacion_establecimientos_delito(dict_delitos=dictio_barrios_ordenado,
                                        dict_establecimientos=dictio_locales_ordenado)"""

    
    # Enviamos como parametro todo el DF de Delitos
    df_subtes = subtes.ejecutar()
    delitos_en_barrio_chico = delitos.loc[delitos.barrio == "balvanera"]
    subtes.cercania_delitos_subtes(df_delitos=delitos_en_barrio_chico, df_subtes=df_subtes, threshold=0.5)
    delitos_en_barrio_chico = delitos.loc[delitos.barrio == "flores"]
    subtes.cercania_delitos_subtes(df_delitos=delitos_en_barrio_chico, df_subtes=df_subtes, threshold=0.5)
    delitos_en_barrio_chico = delitos.loc[delitos.barrio == "belgrano"]
    subtes.cercania_delitos_subtes(df_delitos=delitos_en_barrio_chico, df_subtes=df_subtes, threshold=0.5)

    # Obtenemos un df con todos los delitos en Palermo (sera usado posteriormente)
    delitos_en_palermo = delitos.loc[delitos.barrio == "palermo"]
    # El barrio en los locales bailables se pone con mayuscula
    #locales_bailables.cercania_delitos_locales(delitos_en_palermo, df_locales, barrio="Palermo")

    dictio = franja.ejecutar(delitos)
    graficador.graficar_area(diccionario=dictio, column_name="delitos", 
        titulo_grafico="Delitos segun Franja Horaria", tit_x="Hora", tit_y="Delitos")


    # get all the unique values in the 'Anio' column
    years = delitos['anio'].unique()
    lista_years = []
    for year in years:
        lista_years.append(delitos.loc[delitos.anio == year])

    acum, index_max, max, dictio = calculos.calcular_cantidad_delitos_por_columna(lista=lista_years, columna=years, 
    mensaje="Cantidad de delitos en el año ")

    print("\n\t -------- Cantidad de delitos por año -------- \n")
    total_delitos = delitos.anio.shape[0]
    print("\nCantidad total de delitos: {} y la suma de delitos por año es: {}".format(total_delitos, acum))
    print("\nEl año con mas delitos fue {} con {} delitos".format(years[index_max],
                                                            max))
 
    graficador.graficar_trend(diccionario=dictio, column_name="delitos", 
        titulo_grafico="Tendenecia de Delitos por Año", tit_x="Años", tit_y="Delitos")



    # get all the unique values in the 'Tipo' column
    print("\n\t -------- TIPO DELITOS -------- \n")
    tipos = delitos['tipo'].unique()
    lista_tipo = []
    for tipo in tipos:
        lista_tipo.append(delitos.loc[delitos.tipo == tipo])

    acum, index_max, max, dictio = calculos.calcular_cantidad_delitos_por_columna(lista=lista_tipo, columna=tipos, 
    mensaje="Cantidad de delitos segun el tipo ")

    print("\n\t -------- Cantidad de delitos por tipo -------- \n")
    total_delitos = delitos.tipo.shape[0]
    print("\nCantidad total de delitos: {} y la suma de delitos por tipo es: {}".format(total_delitos, acum))
    print("\nEl tipo de delito mas cometido es {} con {} delitos".format(tipos[index_max],
                                                            max))
 
    graficador.graficar_pie(diccionario=dictio, column_name="delitos", 
        titulo_grafico="Grafico de Tipos de Delito")

    
    # get all the unique values in the 'estacion' column
    estaciones = delitos['estacion'].unique()
    lista_estaciones = []
    for estacion in estaciones:
        lista_estaciones.append(delitos.loc[delitos.estacion == estacion])

    acum, index_max, max, dictio = calculos.calcular_cantidad_delitos_por_columna(lista=lista_estaciones, columna=estaciones, 
    mensaje="Cantidad de delitos en la estación ")

    print("\n\t -------- Cantidad de delitos por estacion del año -------- \n")
    total_delitos = delitos.estacion.shape[0]
    print("\nCantidad total de delitos: {} y la suma de delitos por estacion del año es: {}".format(total_delitos, acum))
    print("\nLa estacion con mas delitos fue {} con {} delitos".format(estaciones[index_max],
                                                            max))
 
    graficador.graficar_pie(diccionario=dictio, column_name="delitos", 
        titulo_grafico="Grafico de Delitos por Estacion")


# get all the unique values in the 'dia' column
    dias = delitos['dia'].unique()
    lista_dias = []
    for dia in dias:
        lista_dias.append(delitos.loc[delitos.dia == dia])

    acum, index_max, max, dictio = calculos.calcular_cantidad_delitos_por_columna(lista=lista_dias, columna=dias, 
    mensaje="Cantidad de delitos en el dia ")

    print("\n\t -------- Cantidad de delitos por dias del año -------- \n")
    total_delitos = delitos.dia.shape[0]
    print("\nCantidad total de delitos: {} y la suma de delitos por dias del año es: {}".format(total_delitos, acum))
    print("\nEl dia con mas delitos fue {} con {} delitos".format(dias[index_max],
                                                            max))
 
    graficador.graficar_pie(diccionario=dictio, column_name="delitos", 
        titulo_grafico="Grafico de Delitos por Dia")

    # Graficar y calcular tendencias de estaciones del año
    graficar_trends(df=delitos, agrupadores=["anio", "estacion"],
                             lista_objetivo_trends=["Verano", "Otoño", "Invierno", "Primavera"],
                             titulo_print="Tendencia de Delitos por Estaciones para cada año")

    # Graficar y calcular tendencias respecto a Homicidios Dolosos y Robos Violentos
    graficar_trends(df=delitos, agrupadores=["anio", "tipo"], 
                            lista_objetivo_trends=["Homicidio", "Robo (con violencia)"],
                            titulo_print="Tendencia de Delitos por Tipo para cada año")
   
 

def graficar_trends(df, agrupadores, lista_objetivo_trends, titulo_print):
    # obtenemos la cantidad de delitos por agrupadores (ejemplo Primavera 2016 = 50000)
    df_agrupada = df.groupby(agrupadores).size().reset_index().rename(columns={0:'count'})
    # Lo parseamos a una lista
    lista_agrupada = list(zip(df_agrupada[agrupadores[0]], df_agrupada[agrupadores[1]], df_agrupada["count"]))
    dictionary_agrupado = utilidades.to_dict_from_list_of_tuples(lista=lista_agrupada)
    # Para cada objetivo (ejemplo Primavera, Otoño, Invierno, Verano) graficamos
    for objetivo in lista_objetivo_trends:
        graficar_trend_por_estacion(dictionary=dictionary_agrupado, 
                            nombre_objetivo=objetivo, titulo_print=titulo_print)


def graficar_trend_por_estacion(dictionary, nombre_objetivo, titulo_print):
    # Obtenemos un diccionario con los años y delitos por cada objetivo
    lista_delitos_x_objetivo = dictionary.get(nombre_objetivo)
    dict_delitos_x_objetivo = utilidades.to_dict_from_list(lista_delitos_x_objetivo)
    
    print("\n\t -------- " + titulo_print + " -------- \n")
    print(nombre_objetivo + " {}".format(dict_delitos_x_objetivo)) # Vemos por consola el detalle de los valores
    titulo_grafico = "Tendencia de Delitos en {} por Año".format(nombre_objetivo)
    graficador.graficar_trend(diccionario=dict_delitos_x_objetivo, column_name="delitos", 
            titulo_grafico=titulo_grafico, tit_x="Años", tit_y="Delitos")


def graficar_two_trends(df, agrupadores, lista_objetivo_trends, titulo_print):
    # obtenemos la cantidad de delitos por agrupadores (ejemplo Primavera 2016 = 50000)
    df_agrupada = df.groupby(agrupadores).size().reset_index().rename(columns={0:'count'})
    # Lo parseamos a una lista
    lista_agrupada = list(zip(df_agrupada[agrupadores[0]], df_agrupada[agrupadores[1]], df_agrupada["count"]))
    dictionary_agrupado = utilidades.to_dict_from_list_of_tuples(lista=lista_agrupada)
    # Para cada objetivo (ejemplo Primavera, Otoño, Invierno, Verano) graficamos
    lista_diccionarios = []
    for objetivo in lista_objetivo_trends:
        lista_delitos_x_objetivo = dictionary_agrupado.get(objetivo)
        dict_delitos_x_objetivo = utilidades.to_dict_from_list(lista_delitos_x_objetivo)
        lista_diccionarios.append([objetivo, dict_delitos_x_objetivo])
    graficar_two_trend_por_estacion(lista=lista_diccionarios, 
                            nombre_objetivo=objetivo, titulo_print=titulo_print)

def graficar_two_trend_por_estacion(lista, nombre_objetivo, titulo_print):
    # Obtenemos un diccionario con los años y delitos por cada objetivo
    dict_delitos_x_objetivo= lista[0][1]
    diccionario_2 = lista[1][1]
    label_d1 = lista[0][0]
    label_d2 = lista[1][0]
    print("\n\t -------- " + titulo_print + " -------- \n")
    print(nombre_objetivo + " {}".format(dict_delitos_x_objetivo)) # Vemos por consola el detalle de los valores
    titulo_grafico = "Tendencia de Delitos en {} vs {} por Franja Horaria".format(label_d1, label_d2)
    graficador.graficar_two_trends(diccionario=dict_delitos_x_objetivo, label_d1=label_d1,
     diccionario_2=diccionario_2, label_d2=label_d2,
     column_name="delitos", 
            titulo_grafico=titulo_grafico, tit_x="Hora", tit_y="Delitos")

def graficar_four_trends(df, agrupadores, lista_objetivo_trends, titulo_print):
    # obtenemos la cantidad de delitos por agrupadores (ejemplo Primavera 2016 = 50000)
    df_agrupada = df.groupby(agrupadores).size().reset_index().rename(columns={0:'count'})
    # Lo parseamos a una lista
    lista_agrupada = list(zip(df_agrupada[agrupadores[0]], df_agrupada[agrupadores[1]], 
                                df_agrupada[agrupadores[2]],
                                df_agrupada["count"]))
    print(lista_agrupada)
    dictionary_agrupado = utilidades.to_dict_from_list_of_tuples_v2(lista=lista_agrupada, cols=4)
    print(dictionary_agrupado)
     # Para cada objetivo (ejemplo Primavera, Otoño, Invierno, Verano) graficamos
    lista_diccionarios = []
    for objetivo in lista_objetivo_trends:
        lista_delitos_x_objetivo = dictionary_agrupado.get(objetivo)
        dict_delitos_x_objetivo = utilidades.to_dict_of_dicts_from_List(lista_delitos_x_objetivo)
        lista_diccionarios.append([objetivo, dict_delitos_x_objetivo])
    print(lista_diccionarios)
    graficar_four_trend_por_anio(lista=lista_diccionarios, 
                            nombre_objetivo=objetivo, titulo_print=titulo_print)


def graficar_four_trend_por_anio(lista, nombre_objetivo, titulo_print):
    # Obtenemos un diccionario con los años y delitos por cada objetivo
    #print(lista[0][0] + lista[1][0])
    titulo_grafico = "Tendencia de Delitos en {} por Franja Horaria para cada año".format(nombre_objetivo)

    for lis in lista:
        diccionario = lis[1]
        label =  lis[0]
        print("\n\t -------- " + titulo_print + " -------- \n")
        print(nombre_objetivo + " {}".format(diccionario)) # Vemos por consola el detalle de los valores
        plt  = graficador.graficar_varias_trends(diccionario=diccionario, label=label, 
        column_name="delitos", titulo_grafico=titulo_grafico, tit_x="Hora", tit_y="Delitos")
    plt.legend()
    plt.show()

    