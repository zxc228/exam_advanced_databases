import sys

if __name__ == '__main__':
    #datos_filtrados = []
    
    for i,l in enumerate(sys.stdin):
        if i == 0:
            continue
        try:
            print(l.split("\t")[1],"\t",float(l.split("\t")[-1][:-2]))
        except Exception as E:
            continue
        
    #print(datos_filtrados)