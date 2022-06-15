from cmath import nan
import pandas as pd
import numpy as np
import common_libs.mapas as plot_map
import common_libs.cleaning_module as cm
import common_libs.calculos_delitos as calculos
import common_libs.utils as utilidades
import common_libs.mapas as plot_map
import common_libs.franja_horaria as franja
import common_libs.graficador as graficador
import os
ABSOLUTE_PATH = os.path.abspath(__file__)
FILE_DIRECTORY = os.path.dirname(ABSOLUTE_PATH)
PARENT_DIRECTORY = os.path.dirname(FILE_DIRECTORY)
CONTAINER_DIRECTORY = os.path.dirname(PARENT_DIRECTORY) 
BASE_PATH_ESTABLECIMIENTOS = CONTAINER_DIRECTORY + "\\datasets\\establecimientos-educativos.csv"

def ejecutar():
    # read in all our data
    establecimientos = pd.read_csv(BASE_PATH_ESTABLECIMIENTOS, index_col=False) 
    # Podriamos especificar un index_col=0 para que el id_mapa sea el indice de nuestra set.
    # Al DS 2021 podriamos agregarle dos columnas mas para no reemplazar todas las comas en la latitud y longitud

    # set seed for reproducibility
    np.random.seed(0) 
    print("Longitud establecimientos: ", establecimientos.shape)
    # Muestra las primeras 5 filas
    print(establecimientos.head())

    # get the number of missing data points per column
    missing_values_count = establecimientos.isnull().sum()

    # cantidad total de valores faltantes
    total_cells = np.product(establecimientos.shape)
    total_missing = missing_values_count.sum()

    percent_missing = (total_missing/total_cells) * 100
    print("\nCantidad de datos faltantes: ", total_missing)
    print("\nPorcentaje de datos faltantes: ", percent_missing)
    # get all the unique values in the 'Barrio' column
    barrios = establecimientos['barrio'].unique()

    lista_barrios = []
    for barrio in barrios:
        lista_barrios.append(establecimientos.loc[establecimientos.barrio == barrio])

    print("\n\t -------- Cantidad de Establecimientos por barrio -------- \n")

    acum, index_max, max, dictio = calculos.calcular_cantidad_delitos_por_columna(lista=lista_barrios, columna=barrios, 
    mensaje="Cantidad de establecimientos educativos en barrio ")

    total_delitos = establecimientos.barrio.shape[0]
    print("\nCantidad total de establecimientos: {} y la suma de establecimientos por barrio es: {}".format(total_delitos, acum))
    print("\nEl barrio con mas establecimientos es {} con {} establecimientos".format(barrios[index_max].upper(),
                                                            max))
    diccionario_ordenado = utilidades.sort_dict_by_values(dictionary=dictio, desc=True)
    diccionario_ordenado = utilidades.keys_a_minusculas(diccionario_ordenado)    
    return diccionario_ordenado

def relacion_establecimientos_delito(dict_delitos, dict_establecimientos):
    merged_dictionary = utilidades.merge_dictionary(dict_1=dict_delitos, 
                                                    dict_2=dict_establecimientos)
    print(merged_dictionary)
