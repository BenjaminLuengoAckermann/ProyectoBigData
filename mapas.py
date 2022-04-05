import matplotlib.pyplot as plt

def plotear(BBox, x, y, titulo):
    ruh_m = plt.imread('C:\\Users\\Usuario\\Desktop\\Real Stuff\\2022\\Big Data\\map_refine.png')
    fig, ax = plt.subplots(figsize = (8,7))
    ax.scatter(x, y, zorder=1, alpha=1, c='orange', s=30)
    # S es el tamaño del punto, alpha el nivel de opacidad
    #ax.scatter(delitos.long, delitos.lat, c=count)
    ax.set_title(titulo)
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')
    plt.show()