import fuzzywuzzy
# function to replace rows in the provided column of the provided dataframe
# that match the provided string above the provided ratio with the provided string
def replace_matches_in_column(df, column, string_to_match, min_ratio):
    # get a list of unique strings
    strings = df[column].unique()
    
    # get the top 10 closest matches to our input string
    matches = fuzzywuzzy.process.extract(string_to_match, strings, 
                                         limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)

    # only get matches with a ratio > 90
    close_matches = [matches[0] for matches in matches if matches[1] >= min_ratio]

    # get the rows of all the close matches in our dataframe
    rows_with_matches = df[column].isin(close_matches)

    # replace all rows with close matches with the input matches 
    df.loc[rows_with_matches, column] = string_to_match
    
    # let us know the function's done
    print("Matches limpios!")

def limpiar(df, column):
    # convert to lower case
    df[column] = df[column].str.lower()
    # remove trailing white spaces
    df[column] = df[column].str.strip()
    # eliminar los NaN
    df = df.dropna(subset=[column], how="all")
    return df

def limpiar_text_sd(df, column):

    print("Cantidad de delitos x franja previo a limpiar {}".format(df[column].shape[0]))

    df[column] = df[column].str.strip()
    #Se eliminan tanto NaNs como valores desconocidos
    if(column == "franja_horaria"):
        df = df.dropna(subset=[column], how="all")
    df.drop(df[df[column] == "S/D"].index, inplace=True) 
    df.drop(df[df[column] == "SD"].index, inplace=True) 

    return df

def limpiar_mayor_menor_a_un_value(df, column, mayor, menor):
    flag = False
    print("Cantidad de delitos por {} previo a limpiar {}".format(column, df[column].shape[0]))
    while flag == False: 
        try:
            df[column] = df[column].astype(float)
            #Se eliminan tanto NaNs como valores desconocidos
            df.drop(df[df[column] > mayor].index, inplace=True) 
            df.drop(df[df[column] < menor].index, inplace=True)
            flag = True
        except:
            #df[column] = df[column].str.strip()
            df.drop(df[df[column] == "S/D"].index, inplace=True) 
            df.drop(df[df[column] == "SD"].index, inplace=True)

    print("Cantidad de delitos por {} POSTERIOR a limpiar {}".format(column, df[column].shape[0]))
    return df