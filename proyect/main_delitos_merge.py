import merged_pkg.delitos_merged_lib as deli
import subtes as sub
import os

ABSOLUTE_PATH = os.path.abspath(__file__)
FILE_DIRECTORY = os.path.dirname(ABSOLUTE_PATH)
PARENT_DIRECTORY = os.path.dirname(FILE_DIRECTORY)


BASE_PATH = PARENT_DIRECTORY + "\\datasets\\delitos_merged.csv"
BASE_PATH_SUBTE = PARENT_DIRECTORY + "\\datasets\\estaciones-de-subte.csv"

print("\n ----------- DELITOS HISTORICOS (2016-2021) --------------- \n")
deli.ejecutar(BASE_PATH)

print("\n ----------- SUBTES --------------- \n")
sub.ejecutar(BASE_PATH_SUBTE)
