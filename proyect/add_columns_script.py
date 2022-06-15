import pandas as pd
import os
import common_libs.cleaning_module as cleaning
import common_libs.add_columns as add_columns

# Script para agregar columnas al dataset y luego exportarlo

# Read the data
ABSOLUTE_PATH = os.path.abspath(__file__)
FILE_DIRECTORY = os.path.dirname(ABSOLUTE_PATH)
PARENT_DIRECTORY = os.path.dirname(FILE_DIRECTORY)

BASE_PATH = PARENT_DIRECTORY + "\\datasets\\delitos_merged.csv"
data = pd.read_csv(BASE_PATH, index_col=False)
print(data.head())
#data = franja.limpiar(data)
data = cleaning.limpiar_text_sd(data, "franja_horaria")
data = cleaning.limpiar_mayor_menor_a_un_value(data, "longitud", mayor=-50, menor=-60)
data = cleaning.limpiar_mayor_menor_a_un_value(data, "latitud", mayor=-30, menor=-40)

# Agregar columnas
data = add_columns.agregar_dia_de_la_semana(data) # data["dia"] y data["dia_numero"]
data = add_columns.agregar_estacion(data) # data["estacion"]

# Exportar CSV
CSV_NAME="delitos_merged_with_more_columns_v4.csv"
data.to_csv(CSV_NAME)
