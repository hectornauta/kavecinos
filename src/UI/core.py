from math import sqrt

def distancia(punto1,punto2):
	return sqrt((punto1[0]-punto2[0])**2 + (punto1[1]-punto2[1])**2)
def vecinos(listaDePuntos,puntoTest,k):
	vecinos = list()
	for punto in listaDePuntos:
		d = distancia(puntoTest,punto)
		vecinos.append((punto,d))
	vecinos.sort(key=lambda tup: tup[1])
	vecinos = vecinos[0:k]
	print(vecinos)
	return vecinos
def prediccion(puntoTest,listadevecinos):
	clases = list()
	for vecino in listadevecinos:
		clases.append(vecino[0][-1])
	print(clases)
	clase = masFrecuente(clases)	
	return clase

def masFrecuente(lista): 
    return max(set(lista), key = lista.count)