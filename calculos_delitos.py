
def calcular_cantidad_delitos_por_barrio(lista, columna, mensaje):
    acum = 0
    max = -1
    index_max = -1
    for i in range(len(lista)):
        delitos_por_barrio = lista[i].shape[0]
        print("\t{}{}: {}".format(mensaje, columna[i].upper(), delitos_por_barrio))
        acum += delitos_por_barrio
        if(i == 0 or delitos_por_barrio >= max):
            max = delitos_por_barrio
            index_max = i
    return acum, index_max, max