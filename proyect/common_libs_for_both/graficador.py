import pandas as pd
import matplotlib.pyplot as plt

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
