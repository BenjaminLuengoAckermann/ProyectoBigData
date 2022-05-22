import sys
import os
ABSOLUTE_PATH = os.path.abspath(__file__)
FILE_DIRECTORY = os.path.dirname(ABSOLUTE_PATH)
PARENT_DIRECTORY = os.path.dirname(FILE_DIRECTORY)
sys.path.insert(0, PARENT_DIRECTORY )
import por_anio_pkg.delitos as deli
import subtes as sub

# La ruta que contiene tanto los proyectos como los datasets
CONTAINER_DIRECTORY = os.path.dirname(PARENT_DIRECTORY)

BASE_PATH = CONTAINER_DIRECTORY + "\\datasets\\delitos_"
BASE_PATH_SUBTE = CONTAINER_DIRECTORY + "\\datasets\\estaciones-de-subte.csv"

#print("\n ----------- 2020 --------------- \n")
#deli.ejecutar(BASE_PATH + "2020.csv", "2020")
print("\n ----------- 2019 --------------- \n")
deli.ejecutar(BASE_PATH + "2019.csv", csv_year="2019")
#print("\n ----------- 2018 --------------- \n")
#deli.ejecutar(BASE_PATH + "2018.csv", csv_year="2018")
"""print("\n ----------- 2017 --------------- \n")
deli.ejecutar(BASE_PATH + "2017.csv", csv_year="2017")
print("\n ----------- 2016 --------------- \n")
deli.ejecutar(BASE_PATH + "2016.csv", csv_year="2016")"""

print("\n ----------- SUBTES --------------- \n")
sub.ejecutar(BASE_PATH_SUBTE)
