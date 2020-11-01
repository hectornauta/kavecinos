from math import sqrt
from collections import Counter

def distancia(punto1,punto2):
	return sqrt((punto1[0]-punto2[0])**2 + (punto1[1]-punto2[1])**2)
def vecinos(listaDePuntos,puntoTest,k):
	vecinos = list()
	for punto in listaDePuntos:
		d = distancia(puntoTest,punto)
		vecinos.append((punto,d))
	vecinos.sort(key=lambda tup: tup[1])
	vecinos = vecinos[0:k]
	#print(vecinos)
	return vecinos
def prediccion(puntoTest,listadevecinos):
	clases = list()
	for vecino in listadevecinos:
		clases.append(vecino[0][-1])
	#print(clases)
	clase = masFrecuente(clases)	
	return clase

def prediccionConCalidad(puntoTest,listadevecinos):
	clases = list()
	for vecino in listadevecinos:
		clases.append(vecino[0][-1])
	clase = masFrecuente(clases)
	
	calidad = clases.count(clase)/len(clases)	
	return ((clase,calidad))

def masFrecuente(lista):
	arreglo = Counter(lista)
	#print(arreglo)
	return max(lista, key=arreglo.get)
	#return max(set(lista), key = lista.count)

def predecirClase(listaDePuntos,puntoTest,k):
	loskvecinos = vecinos(listaDePuntos,puntoTest,k)
	return prediccion(puntoTest,loskvecinos)

def predecirClaseConCalidad(listaDePuntos,puntoTest,k):
	loskvecinos = vecinos(listaDePuntos,puntoTest,k)
	return prediccionConCalidad(puntoTest,loskvecinos)