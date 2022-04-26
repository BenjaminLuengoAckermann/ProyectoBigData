import common_libs_for_both.calculos_delitos as calculos


def limpiar(delitos):

    print("Cantidad de delitos x franja previo a limpiar {}".format(delitos["franja_horaria"].shape[0]))

    delitos["franja_horaria"] = delitos["franja_horaria"].str.strip()
    #Se eliminan tanto NaNs como valores desconocidos
    delitos = delitos.dropna(subset=["franja_horaria"], how="all")
    delitos.drop(delitos[delitos.franja_horaria == "S/D"].index, inplace=True) 
    delitos.drop(delitos[delitos.franja_horaria == "SD"].index, inplace=True) 

    return delitos


def ejecutar(delitos):
    
    franja_horaria = delitos["franja_horaria"].unique()
    franja_horaria.sort()
    print("Cantidad de delitos x franja post limpieza {}".format(delitos["franja_horaria"].shape[0]))

    lista_franja_horarios = []
    for horario in franja_horaria:
        lista_franja_horarios.append(delitos.loc[delitos.franja_horaria == horario])

    print("\n\t -------- Cantidad de delitos por franja horaria -------- \n")

    acum, index_max, max, dict = calculos.calcular_cantidad_delitos_por_columna(lista=lista_franja_horarios,
     columna=franja_horaria, mensaje="\tCantidad de delitos a la hora ")

    total_delitos = delitos.franja_horaria.shape[0]

    #print("\nCantidad total de delitos: {} y la suma de delitos por barrio es: {}".format(total_delitos, acum))
    print("\n La franja horaria con mas delitos es {} hs con {} delitos".format(franja_horaria[index_max].upper(),
                                                            max))

    return dict
