import sys

if __name__ == '__main__':
    #datos_filtrados = []
    nombres_valores = []
    
    for i,l in enumerate(sys.stdin):
        nombre = l.split("\t")[0]
        valor = float(l.split("\t")[1])
        
        if (i == 0) or (nombre != nombres_valores[-1][0]):
            nombres_valores.append([nombre, valor])
        else:
            nombres_valores[-1][1] += valor
    
    for k in nombres_valores:
        print(k[0],k[1])