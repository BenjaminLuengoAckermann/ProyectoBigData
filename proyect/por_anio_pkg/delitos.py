# modules we'll use
from cmath import nan
import pandas as pd
import numpy as np
import fuzzywuzzy
from fuzzywuzzy import process
import common_libs_for_both.cleaning_module as cm
import common_libs_for_both.calculos_delitos as calculos
import common_libs_for_both.mapas as plot_map
import common_libs_for_both.franja_horaria as franja
import common_libs_for_both.graficador as graficador
import matplotlib.pyplot as plt


def ejecutar(ruta, csv_year):
    # read in all our data
    delitos = pd.read_csv(ruta, index_col=False) 
    # Podriamos especificar un index_col=0 para que el id_mapa sea el indice de nuestra set.
    # Al DS 2021 podriamos agregarle dos columnas mas para no reemplazar todas las comas en la latitud y longitud

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
    print("\nEl barrio con mas delitos es {} con {} delitos".format(barrios[index_max].upper(),
                                                            max))

    dict = franja.ejecutar(delitos)
    titulo_grafico = "Delitos segun Franja Horaria - Año " + csv_year
    graficador.graficar_area(diccionario=dict, column_name="delitos", 
        titulo_grafico=titulo_grafico, tit_x="Hora", tit_y="Delitos")


    only_palermo = delitos.loc[delitos.barrio == "palermo"]
    BBox = (only_palermo.longitud.min(), only_palermo.longitud.max(), 
    only_palermo.latitud.min(), only_palermo.latitud.max())
    #print(only_palermo.count())

    print("\n Coordenadas maximas y minimas (definen mapa): {}".format(BBox))
    ruh_m = plt.imread('C:\\Users\\Usuario\\Desktop\\Real Stuff\\2022\\Big Data\\proyect\\map_refine.png')
    fig, ax = plt.subplots(figsize = (8,7))
    ax.scatter(only_palermo.longitud, only_palermo.latitud, zorder=1, alpha= 0.2, c='red', s=5)
    #ax.scatter(delitos.long, delitos.lat, c=count)
    ax.set_title('Distribucion de Delitos - Año ' + csv_year)
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')
    plt.show()