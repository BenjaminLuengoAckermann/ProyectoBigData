from sklearn.metrics.pairwise import haversine_distances

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
import geopy.distance as geo
ABSOLUTE_PATH = os.path.abspath(__file__)
FILE_DIRECTORY = os.path.dirname(ABSOLUTE_PATH)
PARENT_DIRECTORY = os.path.dirname(FILE_DIRECTORY)
CONTAINER_DIRECTORY = os.path.dirname(PARENT_DIRECTORY) 
BASE_PATH_LOCALES = CONTAINER_DIRECTORY + "\\datasets\\locales-bailables.csv"
# Declaramos el DS como variable aca para que se utilice en todos los metodos
LOCALES: pd.DataFrame

def ejecutar():
    # read in all our data
    LOCALES = pd.read_csv(BASE_PATH_LOCALES, index_col=False) 
    # Podriamos especificar un index_col=0 para que el id_mapa sea el indice de nuestra set.
    # Al DS 2021 podriamos agregarle dos columnas mas para no reemplazar todas las comas en la latitud y longitud

    # set seed for reproducibility
    np.random.seed(0) 
    print("Longitud locales bailables: ", LOCALES.shape)
    # Muestra las primeras 5 filas
    print(LOCALES.head())

    # get the number of missing data points per column
    missing_values_count = LOCALES.isnull().sum()

    # cantidad total de valores faltantes
    total_cells = np.product(LOCALES.shape)
    total_missing = missing_values_count.sum()

    percent_missing = (total_missing/total_cells) * 100
    print("\nCantidad de datos faltantes: ", total_missing)
    print("\nPorcentaje de datos faltantes: ", percent_missing)
    # get all the unique values in the 'Barrio' column
    barrios = LOCALES['barrio'].unique()

    lista_barrios = []
    for barrio in barrios:
        lista_barrios.append(LOCALES.loc[LOCALES.barrio == barrio])

    print("\n\t -------- Cantidad de Locales Bailables por barrio -------- \n")

    acum, index_max, max, dictio = calculos.calcular_cantidad_delitos_por_columna(lista=lista_barrios, columna=barrios, 
    mensaje="Cantidad de locales bailables en barrio ")

    total_delitos = LOCALES.barrio.shape[0]
    print("\nCantidad total de locales bailables: {} y la suma de locales bailables por barrio es: {}".format(total_delitos, acum))
    print("\nEl barrio con mas locales bailables es {} con {} locales bailables".format(barrios[index_max].upper(),
                                                            max))
    diccionario_ordenado = utilidades.sort_dict_by_values(dictionary=dictio, desc=True)
    diccionario_ordenado = utilidades.keys_a_minusculas(diccionario_ordenado)    
    return diccionario_ordenado, LOCALES

def relacion_establecimientos_delito(dict_delitos, dict_establecimientos):
    merged_dictionary = utilidades.merge_dictionary(dict_1=dict_delitos, 
                                                    dict_2=dict_establecimientos)
    print(merged_dictionary)


def cercania_delitos_locales(df_delitos, locales, barrio):
    df_locales = locales.loc[locales.barrio == barrio]
    columns_names = []
    for i, j in df_locales.iterrows():
        nombre: str = j["nombre"]
        nombre = nombre.lower()
        nombre = nombre.replace(" ", "_")
        col_latitud = "latitud_{}".format(nombre)
        col_longitud = "longitud_{}".format(nombre)
        col_cercania = "cercania_{}".format(nombre)
        columns_names.append(nombre)
        latitud_value = j["latitud"]
        longitud_value = j["longitud"]
        df_delitos.insert(0, col_latitud, latitud_value)
        df_delitos.insert(0, col_longitud, longitud_value)
        df_delitos.insert(0, col_cercania, 0)

    df_delitos = calcular_cercania_geopy(df=df_delitos, columns_names=columns_names)
    print("\nCantidad total de delitos en {} es: {}".format(barrio, df_delitos.shape[0]))
    utilidades.export_csv(df=df_delitos, CSV_NAME="delitos_cercanos_{}".format(barrio))
    return df_delitos

def calcular_cercania_geopy(df, columns_names):
    for local in columns_names:
        col_latitud = "latitud_{}".format(local)
        col_longitud = "longitud_{}".format(local)
        col_cercania = "cercania_{}".format(local)        
        for i, j in df.iterrows():
            cord_tuple_delito = (j["latitud"], j["longitud"])
            cord_tuple_local = (j[col_latitud], j[col_longitud])
            if(pd.isna(cord_tuple_delito[0]) or pd.isna(cord_tuple_delito[1])):
                continue
            try:
                distancia = geo.geodesic(cord_tuple_delito, cord_tuple_local).km
            except ValueError:
                distancia = 10000000 # valor arbitrario
            if(distancia <= 1):
                df.at[i, col_cercania] = 1
    mostrar_resultados_cercania(df, columns_names)
    return df

def mostrar_resultados_cercania(df, columns_names):
    dictionary_res = {}
    for local in columns_names:
        col_cercania = "cercania_{}".format(local)
        try:
            dictionary_res[col_cercania] = df[col_cercania].value_counts()[1]
        except:
            dictionary_res[col_cercania] = df[col_cercania].value_counts()[0]
    sorted_dict = utilidades.sort_dict_by_values(dictionary=dictionary_res, desc=True)
    print(sorted_dict)

def calcular_cercania():
    # Aqui otra forma de calcular la cercania sin utilizar geopy
    # Este metodo propone usar scikitlearn
    return "https://stackoverflow.com/questions/70941094/how-to-get-the-distance-between-two-geographic-coordinates-of-two-different-data"
