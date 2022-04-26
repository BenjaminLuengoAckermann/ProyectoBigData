def calcular_cantidad_delitos_por_columna(lista, columna, mensaje):
    acum = 0
    max = -1
    index_max = -1
    dict = {}
    for i in range(len(lista)):
        delitos_por_columna = lista[i].shape[0]
        print("\t{}{}: {}".format(mensaje, str(columna[i]).upper(), delitos_por_columna))
        acum += delitos_por_columna
        dict[columna[i]] = delitos_por_columna # Arma un diccionario (key, value) con la columna de interes y su acumulado
        if(i == 0 or delitos_por_columna >= max):
            max = delitos_por_columna
            index_max = i
    return acum, index_max, max, dict
    