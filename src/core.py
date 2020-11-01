from math import sqrt
#from collections import Counter

def distancia(punto1,punto2):
	return sqrt((punto1[0]-punto2[0])**2 + (punto1[1]-punto2[1])**2)
def vecinos(listaDePuntos,puntoTest,k):
	vecinos = []
	#Obtención de la distancia a cada punto
	for punto in listaDePuntos:
		d = distancia(puntoTest,punto)
		instancia = []
		instancia.append(punto)
		instancia.append(d)
		vecinos.append(instancia)
	#Ordenamiento de los puntos según distancia
	vecinos.sort(key = lambda tup: tup[1])
	#Obtención de los k vecinos cercanos
	vecinos = vecinos[0:k]
	return vecinos
def prediccion(puntoTest,listadevecinos):
	#Creación de lista con todas las clases de los vecinos cercanos
	clases = []
	for vecino in listadevecinos:
		clases.append(vecino[0][-1])
	#Obtener clase más frecuente
	clase = masFrecuente(clases)	
	return clase

def prediccionConCalidad(puntoTest,listadevecinos):
	#Creación de lista con todas las clases de los vecinos cercanos
	clases = []
	for vecino in listadevecinos:
		clases.append(vecino[0][-1])
	clase = masFrecuente(clases)
	#Estimación de calidad de la predicción en base al % de la clase escogida respecto del total de vecinos
	calidad = clases.count(clase)/len(clases)	
	return ((clase,calidad))

def masFrecuente(lista):
	#arreglo = Counter(lista)
	#resultado1 = max(lista, key=arreglo.get)
	#return max(lista, key=arreglo.get)
	#resultado2 = max(set(lista), key = lista.count)
	return max(set(lista), key = lista.count)

def predecirClase(listaDePuntos,puntoTest,k):
	loskvecinos = vecinos(listaDePuntos,puntoTest,k)
	return prediccion(puntoTest,loskvecinos)

def predecirClaseConCalidad(listaDePuntos,puntoTest,k):
	loskvecinos = vecinos(listaDePuntos,puntoTest,k)
	return prediccionConCalidad(puntoTest,loskvecinos)