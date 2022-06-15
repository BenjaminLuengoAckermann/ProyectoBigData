import sys
import os
ABSOLUTE_PATH = os.path.abspath(__file__)
FILE_DIRECTORY = os.path.dirname(ABSOLUTE_PATH)
PARENT_DIRECTORY = os.path.dirname(FILE_DIRECTORY)
sys.path.insert(0, PARENT_DIRECTORY)
from calendar import c
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, OneHotEncoder, OrdinalEncoder, minmax_scale
from xgboost import XGBRegressor
import xgboost as xgb
import predicciones as preds
import matplotlib.pyplot as plt
import common_libs.utils as utilidades


# La ruta que contiene tanto los proyectos como los datasets
CONTAINER_DIRECTORY = os.path.dirname(PARENT_DIRECTORY)

BASE_PATH = CONTAINER_DIRECTORY + "\\datasets\\delitos_merged_with_more_columns.csv"
data = pd.read_csv(BASE_PATH, index_col=False)
# Con este comando establecemos el maximo de columnas que se visualizaran (por defecto 20)
#pd.set_option("display.max_columns", 100)
#data = data.sample(n=100000)
print(data.head())

# Diccionario que contendra las predicciones del Tipo
diccionario_predicciones = utilidades.get_diccionario_predicciones(data, "tipo")

# Pasamos de una variable categorica como el tipo a valores numericos para poder entrenar el modelo
ordinal_cols = ["tipo"]
ordinal_encoder = OrdinalEncoder()
data[ordinal_cols] = ordinal_encoder.fit_transform(data[ordinal_cols])

# Escalamos los valores entre 0 y 1 para no "confundir" al modelo
min_max_scaler = MinMaxScaler()
data[["anio", "franja_horaria", "longitud", 
    "latitud"]] = min_max_scaler.fit_transform(data[["anio",
         "franja_horaria", "longitud", "latitud"]])
print(data.sample(n=10))

# Seleccionamos el target (lo que buscamos predecir)
y = data.tipo
print("---Target---")
print(y.head())


# Seleccionamos los predictores o features, con lo que vamos a predecir el target
cols_to_use = ["anio", "franja_horaria", "subtipo", "barrio", "latitud", "longitud", 
                "estacion", "dia"]
X = data[cols_to_use]
print(X.head())


# Separamos datos entre entrenamiento y validacion(porcion de datos no vista para entrenar)
X_train, X_valid, y_train, y_valid = train_test_split(X, y)

# Lista de variables categoricas dentro de los features
one_hot_cols = ["subtipo", "barrio", "estacion", "dia"]

print("Categorical variables:")
print(one_hot_cols)

# Aplicamos one-hot encoder a cada columna categorica
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(X_train[one_hot_cols]))
OH_cols_valid = pd.DataFrame(OH_encoder.transform(X_valid[one_hot_cols]))


# One-hot encoding remueve el indice, lo ponemos de nuevo
OH_cols_train.index = X_train.index
OH_cols_valid.index = X_valid.index


#Le ponemos nombres a las columnas
OH_cols_train.columns = OH_encoder.get_feature_names_out(one_hot_cols)
OH_cols_valid.columns = OH_encoder.get_feature_names_out(one_hot_cols)


# Eliminamos las columnas categoricas y remplazamos con las de one-hot encoding
num_X_train = X_train.drop(one_hot_cols, axis=1)
num_X_valid = X_valid.drop(one_hot_cols, axis=1)


# Añadimos las columnas one-hot encoded a las features numericas
OH_X_train = pd.concat([num_X_train, OH_cols_train], axis=1)
OH_X_valid = pd.concat([num_X_valid, OH_cols_valid], axis=1)




print(OH_X_train.head())


# Entrenamiento del modelo
my_model = XGBRegressor(n_estimators=1000)
my_model.fit(OH_X_train, y_train, 
             early_stopping_rounds=5, 
             eval_set=[(OH_X_valid, y_valid)],
             verbose=False)

predictions = my_model.predict(OH_X_valid)

# Calculo de metricas
print("Mean Absolute Error: " + str(mean_absolute_error(predictions, y_valid)))
print("RMSE: " + str(np.sqrt(mean_squared_error(predictions, y_valid))))
print("Max: {} --- Min: {}".format(predictions.max(), predictions.min()))

# Obtiene el arbol de decision del modelo
xgb.plot_tree(my_model,num_trees=1)
plt.rcParams['figure.figsize'] = [50, 50]
plt.rcParams['figure.dpi'] = 140
plt.rcParams['savefig.dpi'] = 650
plt.show()


for i in range (10000): 
    row = OH_X_train.sample() # Toma una fila aleatoria del modelo
    #print(row)
    row["anio"] = 1.2 # Año 2022
    row["franja_horaria"] = 0.96 # 22hs (valor escalado) 
    # Asignamos el dia viernes a la fila obtenida
    day_cols = ["dia_Monday", "dia_Tuesday", "dia_Wednesday", "dia_Thursday", 
                    "dia_Friday", "dia_Saturday", "dia_Sunday"]
    row[day_cols]  = row[day_cols].replace({1 : 0})
    row["dia_Friday"] = row["dia_Friday"].replace({0 : 1})
    #print(row)
    # Realiza la predicion en base a los datos mostrados de la row
    predictions_2022 = my_model.predict(row) 
    row["tipo"]=predictions_2022

    # Volvemos a los valores normales de los campos (estaban entre 0 y 1)
    row[["anio", "franja_horaria", "longitud", 
        "latitud"]] = min_max_scaler.inverse_transform(row[["anio",
        "franja_horaria", "longitud", "latitud"]])
    #print("Prediccion: {}".format(predictions_2022))

    # Redondedamos el año y la franja ya  que el min_max_scaler devuelve valores flotantes
    row[["anio", "franja_horaria"]] = np.round(row[["anio", "franja_horaria"]], decimals=0)

    # Convertimos el Tipo en un valor categorico de nuevo (de int a la string correspondiente)
    row[["tipo"]] = ordinal_encoder.inverse_transform(row[["tipo"]])
    """for i, j in row.iterrows():
        print(i)
        print(j)"""
    prediccion_final = row[["tipo"]].values[0][0]
    """print("El delito mas probable a ocurrir un Viernes por la Noche ({} hs) es: {}".
                    format(row["franja_horaria"].values[0], 
                            prediccion_final) )"""
    diccionario_predicciones[prediccion_final] += 1
print(diccionario_predicciones)

