import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor
import os
import common_libs.franja_horaria as franja
# Read the data
ABSOLUTE_PATH = os.path.abspath(__file__)
FILE_DIRECTORY = os.path.dirname(ABSOLUTE_PATH)
PARENT_DIRECTORY = os.path.dirname(FILE_DIRECTORY)

BASE_PATH = PARENT_DIRECTORY + "\\datasets\\delitos_merged.csv"
data = pd.read_csv(BASE_PATH, index_col=False)
print(data.head())
data = franja.limpiar(data)

# Select target
y = data.franja_horaria

# Select subset of predictors
cols_to_use = ["anio", "tipo", "subtipo"]
X = data[cols_to_use]
#X = data.drop(["franja_horaria"], axis=1)

# Separate data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y)

# Get list of categorical variables
one_hot_cols = ["tipo", "subtipo"]

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



my_model = XGBRegressor(n_estimators=500)
my_model.fit(OH_X_train, y_train, 
             early_stopping_rounds=5, 
             eval_set=[(OH_X_valid, y_valid)],
             verbose=False)

predictions = my_model.predict(OH_X_valid)
print("Mean Absolute Error: " + str(mean_absolute_error(predictions, y_valid)))
print(predictions)