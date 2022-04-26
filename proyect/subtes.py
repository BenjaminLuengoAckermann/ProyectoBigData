from cmath import nan
import pandas as pd
import numpy as np
import fuzzywuzzy
from fuzzywuzzy import process
import common_libs_for_both.mapas as plot_map
def ejecutar(ruta):
    # read in all our data
    subtes = pd.read_csv(ruta, index_col=False) 
    # Podriamos especificar un index_col=0 para que el id_mapa sea el indice de nuestra set.
    # Al DS 2021 podriamos agregarle dos columnas mas para no reemplazar todas las comas en la latitud y longitud

    # set seed for reproducibility
    np.random.seed(0) 
    print("Longitud subtes: ", subtes.shape)
    # Muestra las primeras 5 filas
    print(subtes.head())

    # get the number of missing data points per column
    missing_values_count = subtes.isnull().sum()

    # cantidad total de valores faltantes
    total_cells = np.product(subtes.shape)
    total_missing = missing_values_count.sum()

    percent_missing = (total_missing/total_cells) * 100
    print("\nCantidad de datos faltantes: ", total_missing)
    print("\nPorcentaje de datos faltantes: ", percent_missing)

    BBox = (subtes.longitud.min(), subtes.longitud.max(), 
    subtes.latitud.min(), subtes.latitud.max())

    print(BBox)
    plot_map.plotear(BBox, x=subtes.longitud, y=subtes.latitud, titulo="Distribucion de Bocas de Subtes")