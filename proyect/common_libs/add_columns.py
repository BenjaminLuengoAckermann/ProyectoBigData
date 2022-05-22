
from sqlalchemy import null
from datetime import datetime, date
import calendar
import numpy as np
import pandas as pd

# Este metodo recorre el DataFrame pasado por parametro y agrega en cada fila
# segun la fecha de la misma, la estacion correspondiente
def agregar_estacion(df):
    df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m-%d").dt.date
    estaciones_list = []
    for i, j in df.iterrows():
        fecha = j["fecha"]
        #fecha = str(fecha).split("T")[0]
        #fecha = pd.to_datetime(fecha, format="%Y-%m-%d")
        estacion = estacion_segun_fecha(fecha)
        estaciones_list.append(estacion)
    df["estacion"] = estaciones_list
    return df

# Este metodo recorre el DataFrame pasado por parametro y agrega en cada fila
# dos columnas que dependen del valor de la fecha: el dia numerico de la semana
# y el nombre de ese dia
def agregar_dia_de_la_semana(df):
    day_name_list = []
    day_number_list = []
    for i, j in df.iterrows():
        fecha = j["fecha"]
        fecha = str(fecha).split("T")[0]
        day = pd.Timestamp(fecha)
        day_name_list.append(day.day_name())
        day_number_list.append(day.dayofweek)
    df["dia"] = day_name_list
    df["dia_numero"] = day_number_list

    return df


def estacion_segun_fecha(fecha):
    Y = 2000 # año bisiesto cualquiera para permitir el input X-02-29
    estaciones = {'Otoño': (date(Y,  3, 21),  date(Y,  6, 20)),
           'Invierno': (date(Y,  6, 21),  date(Y,  9, 22)),
           'Primavera': (date(Y,  9, 23),  date(Y, 12, 20))}
    # Reemplazamos el año en la fecha que viene por parametro para que se pueda comparar
    fecha = fecha.replace(year=Y)

    for estacion, (estacion_inicio, estacion_fin) in estaciones.items():
        if fecha >= estacion_inicio and fecha <= estacion_fin:
            return estacion
    else:
        return "Verano"
