import merged_pkg.delitos_merged_lib as deli
import subtes as sub

BASE_PATH = r"C:\\Users\\Usuario\\Desktop\\Real Stuff\\2022\\Big Data\\datasets\\delitos_merged.csv"
BASE_PATH_SUBTE = r"C:\\Users\\Usuario\\Desktop\\Real Stuff\\2022\\Big Data\\datasets\\estaciones-de-subte.csv"

print("\n ----------- DELITOS HISTORICOS (2016-2021) --------------- \n")
deli.ejecutar(BASE_PATH)

print("\n ----------- SUBTES --------------- \n")
sub.ejecutar(BASE_PATH_SUBTE)
