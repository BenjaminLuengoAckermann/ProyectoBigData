import delitos as deli
import subtes as sub

BASE_PATH = r"C:\\Users\\Usuario\\Desktop\\Real Stuff\\2022\\Big Data\\delitos_"
BASE_PATH_SUBTE = r"C:\\Users\\Usuario\\Desktop\\Real Stuff\\2022\\Big Data\\estaciones-de-subte.csv"

#print("\n ----------- 2020 --------------- \n")
#deli.ejecutar(BASE_PATH + "2020.csv")
print("\n ----------- 2019 --------------- \n")
deli.ejecutar(BASE_PATH + "2019.csv")
#print("\n ----------- 2018 --------------- \n")
#deli.ejecutar(BASE_PATH + "2018.csv")
"""print("\n ----------- 2017 --------------- \n")
deli.ejecutar(BASE_PATH + "2017.csv")
print("\n ----------- 2016 --------------- \n")
deli.ejecutar(BASE_PATH + "2016.csv")"""

print("\n ----------- SUBTES --------------- \n")
sub.ejecutar(BASE_PATH_SUBTE)
