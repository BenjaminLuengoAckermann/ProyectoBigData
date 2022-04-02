
def calcular_cantidad_delitos_por_barrio(lista_barrios, barrios):
    acum = 0
    max = -1
    index_max = -1
    for i in range(len(lista_barrios)):
        delitos_por_barrio = lista_barrios[i].shape[0]
        print("\tCantidad de delitos en barrio {}: {}".format(barrios[i].upper(), delitos_por_barrio))
        acum += delitos_por_barrio
        if(i == 0 or delitos_por_barrio >= max):
            max = delitos_por_barrio
            index_max = i
    return acum, index_max, max