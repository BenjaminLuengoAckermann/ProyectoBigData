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
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, minmax_scale
from xgboost import XGBRegressor
import xgboost as xgb
import os
import common_libs.franja_horaria as franja
import common_libs.cleaning_module as cleaning
import matplotlib.pyplot as plt


# La ruta que contiene tanto los proyectos como los datasets
CONTAINER_DIRECTORY = os.path.dirname(PARENT_DIRECTORY)

BASE_PATH = CONTAINER_DIRECTORY + "\\datasets\\delitos_merged_with_more_columns.csv"
data = pd.read_csv(BASE_PATH, index_col=False)
# Con este comando establecemos el maximo de columnas que se visualizaran (por defecto 20)
#pd.set_option("display.max_columns", 100)
print(data.head())

# Scaler
min_max_scaler = MinMaxScaler()
data[["anio", "franja_horaria", 
"longitud", "latitud"]] = min_max_scaler.fit_transform(data[["anio", "franja_horaria",
                             "longitud", "latitud"]])
print(data.head())

# Select target
y = data.franja_horaria

# Select subset of predictors
cols_to_use = ["anio", "tipo", "subtipo", "barrio", "latitud", "longitud", "estacion", "dia"]
X = data[cols_to_use]
print(X.head())


# Separate data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y)

# Get list of categorical variables
one_hot_cols = ["tipo", "subtipo", "barrio", "estacion", "dia"]

print("Categorical variables:")
print(one_hot_cols)

# Apply one-hot encoder to each column with categorical data
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(X_train[one_hot_cols]))
OH_cols_valid = pd.DataFrame(OH_encoder.transform(X_valid[one_hot_cols]))

# One-hot encoding removed index; put it back
OH_cols_train.index = X_train.index
OH_cols_valid.index = X_valid.index

#Le ponemos nombres a las columnas
OH_cols_train.columns = OH_encoder.get_feature_names_out(one_hot_cols)
OH_cols_valid.columns = OH_encoder.get_feature_names_out(one_hot_cols)

# Remove categorical columns (will replace with one-hot encoding)
num_X_train = X_train.drop(one_hot_cols, axis=1)
num_X_valid = X_valid.drop(one_hot_cols, axis=1)

# Add one-hot encoded columns to numerical features
OH_X_train = pd.concat([num_X_train, OH_cols_train], axis=1)
OH_X_valid = pd.concat([num_X_valid, OH_cols_valid], axis=1)




print(OH_X_train.head())



my_model = XGBRegressor(n_estimators=1000)
my_model.fit(OH_X_train, y_train, 
             early_stopping_rounds=5, 
             eval_set=[(OH_X_valid, y_valid)],
             verbose=False)

predictions = my_model.predict(OH_X_valid)
print("Mean Absolute Error: " + str(mean_absolute_error(predictions, y_valid)))
print("RMSE: " + str(np.sqrt(mean_squared_error(predictions, y_valid))))
print("Max: {} --- Min: {}".format(predictions.max(), predictions.min()))


xgb.plot_tree(my_model,num_trees=1)
plt.rcParams['figure.figsize'] = [50, 50]
plt.rcParams['figure.dpi'] = 140
plt.rcParams['savefig.dpi'] = 650
plt.show()


# Predicciones
row = OH_X_train.sample() # Toma una fila aleatoria del modelo
print(row)
row["anio"] = 1.2 # 2022
print(row)
predictions_2022 = my_model.predict(row)
row["franja_horaria"]=predictions_2022
row[["anio", "franja_horaria", "longitud", 
    "latitud"]] = min_max_scaler.inverse_transform(row[["anio",
     "franja_horaria", "longitud", "latitud"]])
print(predictions_2022)
row[["anio", "franja_horaria"]] = np.round(row[["anio", "franja_horaria"]], decimals=0)
for i, j in row.iterrows():
    print(i)
    print(j)
 
# Another Model
"""my_model_2 = LogisticRegression()
my_model_2.fit(OH_X_train, y_train)

# make a prediction
predictions_2 = my_model_2.predict(OH_X_valid)
print(predictions_2)
# make a prediction
predictions_probabilities = my_model_2.predict_proba(OH_X_valid)
# show the inputs and predicted probabilities
for i in range(5):
	print("X=%s, Predicted=%s" % (predictions_2[i], predictions_probabilities[i]))

print("Mean Absolute Error Model 2: " + str(mean_absolute_error(predictions_2, y_valid)))"""
