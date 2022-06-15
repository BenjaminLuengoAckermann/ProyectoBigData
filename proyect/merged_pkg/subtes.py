from cmath import nan
from typing import Dict
import pandas as pd
import numpy as np
import fuzzywuzzy
from fuzzywuzzy import process
import common_libs.mapas as plot_map
import common_libs.utils as utilidades 
import geopy.distance as geo
import os
ABSOLUTE_PATH = os.path.abspath(__file__)
FILE_DIRECTORY = os.path.dirname(ABSOLUTE_PATH)
PARENT_DIRECTORY = os.path.dirname(FILE_DIRECTORY)
CONTAINER_DIRECTORY = os.path.dirname(PARENT_DIRECTORY) 
BASE_PATH_SUBTE = CONTAINER_DIRECTORY + "\\datasets\\estaciones-de-subte.csv"

def ejecutar():
    # read in all our data
    # read in all our data
    SUBTES = pd.read_csv(BASE_PATH_SUBTE, index_col=False)
    # Podriamos especificar un index_col=0 para que el id_mapa sea el indice de nuestra set.
    # Al DS 2021 podriamos agregarle dos columnas mas para no reemplazar todas las comas en la latitud y longitud

    # set seed for reproducibility
    np.random.seed(0) 
    print("Longitud subtes: ", SUBTES.shape)
    # Muestra las primeras 5 filas
    print(SUBTES.head())

    # get the number of missing data points per column
    missing_values_count = SUBTES.isnull().sum()

    # cantidad total de valores faltantes
    total_cells = np.product(SUBTES.shape)
    total_missing = missing_values_count.sum()

    percent_missing = (total_missing/total_cells) * 100
    print("\nCantidad de datos faltantes: ", total_missing)
    print("\nPorcentaje de datos faltantes: ", percent_missing)

    """BBox = (SUBTES.longitud.min(), SUBTES.longitud.max(), 
    SUBTES.latitud.min(), SUBTES.latitud.max())

    print(BBox)
    plot_map.plotear(BBox, x=SUBTES.longitud, y=SUBTES.latitud, titulo="Distribucion de Bocas de Subtes")"""
    return SUBTES

def cercania_delitos_subtes(df_delitos, df_subtes, threshold):
    nombres_estaciones = {}
    for i, j in df_subtes.iterrows():
        # Tomamos los campos con los que pondremos nombres a las columnas
        estacion: str = j["estacion"]
        linea: str = j["linea"]
        # Formateamos
        linea = linea.lower()
        estacion = estacion.lower()
        estacion = estacion.replace(" ", "_")
        estacion = estacion + "_" + linea
        # Creamos nombres campos
        col_latitud = "latitud_{}".format(estacion)
        col_longitud = "longitud_{}".format(estacion)
        col_cercania = "cercania_{}".format(estacion)
        latitud_value = j["latitud"]
        longitud_value = j["longitud"]
        # Diccionario cuya key es el nombre de la estacion y contiene la lat y long como value
        nombres_estaciones[estacion] = (latitud_value, longitud_value)

        # Insertamos en el df las nuevas columnas
        #df_delitos.insert(0, col_latitud, latitud_value)
        #df_delitos.insert(0, col_longitud, longitud_value)
        #df_delitos.insert(0, col_cercania, 0)

    df_delitos = calcular_cercania_geopy(df=df_delitos, diccionario_estaciones=nombres_estaciones,
            threshold=threshold)
    print("\nCantidad total de delitos en las estaciones es: {}".format(df_delitos.shape[0]))
    utilidades.export_csv(df=df_delitos, CSV_NAME="delitos_cercanos_subtes")
    return df_delitos

def calcular_cercania_geopy(df, diccionario_estaciones: Dict, threshold):
    diccionario_cant_cercanos = {}
    for estacion in diccionario_estaciones.keys():
        col_latitud = "latitud_{}".format(estacion)
        col_longitud = "longitud_{}".format(estacion)
        col_cercania = "cercania_{}".format(estacion)  
        diccionario_cant_cercanos[estacion] = 0      
        for i, j in df.iterrows():
            cord_tuple_delito = (j["latitud"], j["longitud"])
            cord_tuple_local = diccionario_estaciones.get(estacion)
            if(pd.isna(cord_tuple_delito[0]) or pd.isna(cord_tuple_delito[1])):
                continue
            try:
                distancia = geo.geodesic(cord_tuple_delito, cord_tuple_local).km
            except ValueError:
                distancia = threshold + 10000 # valor arbitrario
            if(distancia <= threshold):
                #df.at[i, col_cercania] = 1
                diccionario_cant_cercanos[estacion] += 1
    #mostrar_resultados_cercania(df, diccionario_estaciones)
    print(diccionario_cant_cercanos)
    print(utilidades.sort_dict_by_values(diccionario_cant_cercanos, desc=True))
    return df

def mostrar_resultados_cercania(df, columns_names):
    dictionary_res = {}
    for estacion in columns_names:
        col_cercania = "cercania_{}".format(estacion)
        try:
            dictionary_res[col_cercania] = df[col_cercania].value_counts()[1]
        except:
            dictionary_res[col_cercania] = df[col_cercania].value_counts()[0]
    sorted_dict = utilidades.sort_dict_by_values(dictionary=dictionary_res, desc=True)
    print(sorted_dict)