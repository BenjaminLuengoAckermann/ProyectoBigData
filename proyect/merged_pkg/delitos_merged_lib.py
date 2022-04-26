# modules we'll use
from cmath import nan
import pandas as pd
import numpy as np
import fuzzywuzzy
from fuzzywuzzy import process
import common_libs.cleaning_module as cm
import common_libs.calculos_delitos as calculos
import common_libs.mapas as plot_map
import common_libs.franja_horaria as franja
import common_libs.graficador as graficador
import matplotlib.pyplot as plt


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

    # get all the unique values in the 'Barrio' column
    barrios = delitos['barrio'].unique()

    delitos = franja.limpiar(delitos)

    



    """print("\n ---- Barrios limpios ---- {}\n".format(len(barrios)))
    for barrio in barrios:
        print(barrio)"""

    lista_barrios = []
    for barrio in barrios:
        lista_barrios.append(delitos.loc[delitos.barrio == barrio])

    print("\n\t -------- Cantidad de delitos por barrio -------- \n")

    acum, index_max, max, dict = calculos.calcular_cantidad_delitos_por_columna(lista=lista_barrios, columna=barrios, 
    mensaje="Cantidad de delitos en barrio ")

    total_delitos = delitos.barrio.shape[0]
    print("\nCantidad total de delitos: {} y la suma de delitos por barrio es: {}".format(total_delitos, acum))
    print("\nEl barrio con mas delitos {} con {} delitos".format(barrios[index_max].upper(),
                                                            max))
   
    graficador.graficar_pie(diccionario=dict, column_name="delitos", titulo_grafico="Grafico de Delitos por Barrio")


    
    dict = franja.ejecutar(delitos)
    graficador.graficar_area(diccionario=dict, column_name="delitos", 
        titulo_grafico="Delitos segun Franja Horaria", tit_x="Hora", tit_y="Delitos")


    # get all the unique values in the 'Anio' column
    years = delitos['anio'].unique()
    lista_years = []
    for year in years:
        lista_years.append(delitos.loc[delitos.anio == year])

    acum, index_max, max, dict = calculos.calcular_cantidad_delitos_por_columna(lista=lista_years, columna=years, 
    mensaje="Cantidad de delitos en el año ")

    print("\n\t -------- Cantidad de delitos por año -------- \n")
    total_delitos = delitos.anio.shape[0]
    print("\nCantidad total de delitos: {} y la suma de delitos por año es: {}".format(total_delitos, acum))
    print("\nEl año con mas delitos fue {} con {} delitos".format(years[index_max],
                                                            max))
 
    graficador.graficar_trend(diccionario=dict, column_name="delitos", 
        titulo_grafico="Tendenecia de Delitos por Año", tit_x="Años", tit_y="Delitos")



    # get all the unique values in the 'Tipo' column
    print("\n\t -------- TIPO DELITOS -------- \n")
    tipos = delitos['tipo'].unique()
    lista_tipo = []
    for tipo in tipos:
        lista_tipo.append(delitos.loc[delitos.tipo == tipo])

    acum, index_max, max, dict = calculos.calcular_cantidad_delitos_por_columna(lista=lista_tipo, columna=tipos, 
    mensaje="Cantidad de delitos segun el tipo ")

    print("\n\t -------- Cantidad de delitos por tipo -------- \n")
    total_delitos = delitos.tipo.shape[0]
    print("\nCantidad total de delitos: {} y la suma de delitos por tipo es: {}".format(total_delitos, acum))
    print("\nEl tipo de delito mas cometido es {} con {} delitos".format(tipos[index_max],
                                                            max))
 
    graficador.graficar_pie(diccionario=dict, column_name="delitos", 
        titulo_grafico="Grafico de Tipos de Delito")