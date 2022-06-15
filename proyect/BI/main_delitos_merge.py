import sys
import os
ABSOLUTE_PATH = os.path.abspath(__file__)
FILE_DIRECTORY = os.path.dirname(ABSOLUTE_PATH)
PARENT_DIRECTORY = os.path.dirname(FILE_DIRECTORY)
sys.path.insert(0, PARENT_DIRECTORY )
import merged_pkg.delitos_merged_lib  as deli
import merged_pkg.subtes as sub

# La ruta que contiene tanto los proyectos como los datasets
CONTAINER_DIRECTORY = os.path.dirname(PARENT_DIRECTORY) 

BASE_PATH = CONTAINER_DIRECTORY + "\\datasets\\delitos_merged_with_more_columns.csv"
BASE_PATH_ESTABLECIMIENTOS = CONTAINER_DIRECTORY + "\\datasets\\establecimientos-educativos-csv.csv"

print("\n ----------- DELITOS HISTORICOS (2016-2021) --------------- \n")
deli.ejecutar(BASE_PATH)

"""print("\n ----------- SUBTES --------------- \n")
sub.ejecutar()"""
