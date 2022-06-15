from locale import normalize
from unidecode import unidecode

def to_dict_from_list_of_tuples(lista):
    dictionary = {}
    for tuplas in lista:
            if(tuplas[1] in dictionary):
                dictionary[tuplas[1]].append([tuplas[0], tuplas[2]])
            else:
                dictionary[tuplas[1]] = [[tuplas[0], tuplas[2]]]
    return dictionary

def to_dict_from_list_of_tuples_v2(lista, cols):
    dictionary = {}
    for tuplas in lista:
            if(tuplas[1] in dictionary):
                dictionary[tuplas[1]].append([tuplas[cols-cols], tuplas[2], tuplas[3]])
            else:
                dictionary[tuplas[1]] = [[tuplas[cols-cols], tuplas[2], tuplas[3]]]
    return dictionary

def to_dict_from_list(lista):
    dictionary = {}
    for a in lista:
        dictionary[a[0]] = a[1]
    return dictionary

def to_dict_of_dicts_from_List(lista):
    dictionary = {}
    for a in lista:
        if(a[0] in dictionary):
            dictionary[a[0]].append([a[1], a[2]])
        else:
            dictionary[a[0]] = [[a[1], a[2]]]
    return dictionary 

def sort_dict_by_values(dictionary, desc):
    diccionario_ordenado = {}
    keys_ordenadas = sorted(dictionary, key=dictionary.get, reverse=desc)
    for w in keys_ordenadas:
        diccionario_ordenado[w] = dictionary[w]
    return diccionario_ordenado

# Metodo que hace el merge de dos diccionarios, creando un 
# vector con los values de las keys repetidas en ellos
def merge_dictionary(dict_1, dict_2):
    dict_1_normalized = normalize_keys(dict_1)
    dict_2_normalized = normalize_keys(dict_2)
    dict_merged = {**dict_1_normalized, **dict_2_normalized}
    for key, value in dict_merged.items():
        if key in dict_1_normalized and key in dict_2_normalized:
               dict_merged[key] = [value , dict_1_normalized[key]]
    return dict_merged

# Este metodo transforma las keys de los diccionarios en strings sin tildes
def normalize_keys(dictionary):
    normalized_dict = {}
    keys = dictionary.keys()
    for w in keys:
        normalized_dict[unidecode(w)] = dictionary[w]
    return normalized_dict

# Este metodo pasa todas las keys a minusculas (para no tener problemas de compatiblidad)
def keys_a_minusculas(dictionary):
    keys = dictionary.copy().keys()
    for key in keys:
        dictionary[str(key).lower()] = dictionary.pop(key)
    return dictionary


# Este metodo permite obtener un diccionario que servira de contador para las predicciones
def get_diccionario_predicciones(df, column):
    diccionario_predicciones = {}
    tipos = df[column].unique()
    for tipo in tipos:
        diccionario_predicciones[tipo] = 0
    return diccionario_predicciones

def export_csv(df, CSV_NAME):
    df.to_csv(CSV_NAME + ".csv")