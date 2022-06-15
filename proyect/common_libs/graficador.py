import numpy
import pandas as pd
import matplotlib.pyplot as plt
import squarify as squarify

def graficar_trend(diccionario, column_name, titulo_grafico, tit_x, tit_y):
    graf = pd.DataFrame.from_dict(diccionario, orient='index', columns=[column_name])
    graf.plot(y=column_name, kind="line", marker="o")
    plt.title(titulo_grafico)
    plt.xlabel(tit_x)
    plt.ylabel(tit_y)
    plt.show()

def graficar_pie(diccionario, column_name, titulo_grafico):
    graf = pd.DataFrame.from_dict(diccionario, orient='index', columns=[column_name])
    graf.plot(kind="pie", y=column_name, legend=True, figsize=(12, 8), 
                    autopct='%1.1f%%', shadow=True, startangle=0)
    plt.title(titulo_grafico)
    plt.show()

def graficar_area(diccionario, column_name, titulo_grafico, tit_x, tit_y):
    graf = pd.DataFrame.from_dict(diccionario, orient='index', columns=[column_name])
    graf.index.name = "index"
    graf.sort_index(axis=0, level="index")
    print(graf)

    graf.plot.area(y=column_name)
    idx = []
    for i in range(0,24):
        idx.append(i)


    #print(graf[0])
    """plt.xticks(ticks=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
     labels=idx, rotation="vertical")"""
    plt.title(titulo_grafico)
    plt.xlabel(tit_x)
    plt.ylabel(tit_y)
    plt.show()

def graficar_tree_map(diccionario, column_name, titulo_grafico):
    # Prepare Data
    graf = pd.DataFrame.from_dict(diccionario, orient='index', columns=[column_name])
    print(graf)
    labels = graf.apply(lambda x: str(x.name) + "\n (" + str(x[0]) + ")", axis=1)
    sizes = graf[column_name].values.tolist()
    colors = [plt.cm.Spectral(i/float(len(labels))) for i in range(len(labels))]

    # Draw Plot
    plt.figure(figsize=(12,8), dpi= 80)
    squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8)

    # Decorate
    plt.title(titulo_grafico)
    plt.axis('off')
    plt.show()

def graficar_two_trends(diccionario, label_d1, diccionario_2, label_d2, 
        column_name, titulo_grafico, tit_x, tit_y):
    graf = pd.DataFrame.from_dict(diccionario, orient='index', columns=[column_name])
    plt.plot(diccionario.keys(), diccionario.values(), 'r', label=label_d1, marker=".")
    plt.title(titulo_grafico)
    plt.xlabel(tit_x)
    plt.ylabel(tit_y)
    graf2 = pd.DataFrame.from_dict(diccionario_2, orient='index', columns=[column_name])
    plt.plot(diccionario_2.keys(), diccionario_2.values(), 'b', label=label_d2, marker=".")
    plt.legend()
    plt.show()

def graficar_varias_trends(diccionario, label, 
        column_name, titulo_grafico, tit_x, tit_y):
    
    print(diccionario.keys())
    print(diccionario.values())
    for keys in diccionario.keys():
        label=keys
        x = []
        y = []
        for lista in diccionario[keys]:
            y.append(lista[1])
            x.append(lista[0])

        print(x)
        print(y)
        colour = (numpy.random.random(), numpy.random.random(), numpy.random.random())
        plt.plot(x, y, label=label, c=colour, marker=".")
    
    
    plt.title(titulo_grafico)
    plt.xlabel(tit_x)
    plt.ylabel(tit_y)
    return plt
    