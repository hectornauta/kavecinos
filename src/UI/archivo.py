import csv

class Archivo():
    def __init__(self, ruta_de_archivo):
        self.ruta = ruta_de_archivo
        self.datos = []
        self.columnas = [] 
        self.clases = []
        self.numfilas = 0
        self.numcolumnas = 0
        self.x = []
        self.y = []
        self.clases = []
    def abrir(self):
        with open(self.ruta, encoding='utf8') as csvfile:
	        self.datos = list(csv.reader(csvfile,delimiter=';'))
        self.columnas = self.datos[0]
        self.datos.remove(self.datos[0])
        self.numfilas = len(self.datos)
        self.numcolumnas = len(self.datos[0])
        for dato in self.datos:
            self.x.append(float(dato[0]))
            self.y.append(float(dato[1]))
            self.clases.append(dato[2])
    def datos(self):
        return self.datos