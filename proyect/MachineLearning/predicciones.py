import pandas as pd

def predecir_delito_viernes_a_la_noche(modelo_tipo, df):
    pd.set_option("display.max_columns", 100)
    print("\n ---- PREDICCION DELITO MAS PROBABLE UN VIERNES POR LA NOCHE ---- \n")
    row = df.sample() # Toma una fila aleatoria del modelo
    row["anio"] = 1.2 # Año 2022
    row["franja_horaria"] = 22
    day_cols = ["dia_Monday", "dia_Tuesday", "dia_Wednesday", "dia_Thursday", 
                    "dia_Saturday", "dia_Sunday"]
    df[day_cols]  = df[day_cols].replace({1 : 0})
    row["dia_Friday"] = 1.0 # Dia viernes
    print(row)
    predictions_2022 = modelo_tipo.predict(row)
    row["tipo"]=predictions_2022
    print("\nPRINT DE PREDICCION")
    print(predictions_2022)
    return row

