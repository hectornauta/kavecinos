import csv

#TODO:Borrar las cosas de datos porque las tiene la clase Datos ahora
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
    def abrir(self,separador):
        with open(self.ruta, encoding='utf8') as csvfile:
	        self.datos = list(csv.reader(csvfile,delimiter=separador))
        self.columnas = self.datos[0]
        self.datos.remove(self.datos[0])
        self.numfilas = len(self.datos)
        self.numcolumnas = len(self.datos[0])
        for dato in self.datos:
            self.x.append(float(dato[0]))
            self.y.append(float(dato[1]))
            self.clases.append(dato[2])
    def datosDeEntrenamiento(self,porcentajeEntrenamiento):
        self.datosEntrenamiento = self.datos[0:(int((self.numfilas*porcentajeEntrenamiento)/100))]
        self.datosEntrenamientoX = list()
        self.datosEntrenamientoY = list()
        self.datosEntrenamientoClases = list()
        for dato in self.datosEntrenamiento:
            dato[0] = float(dato[0])
            dato[1] = float(dato[1])
        for dato in self.datosEntrenamiento:
            self.datosEntrenamientoX.append(float(dato[0]))
            self.datosEntrenamientoY.append(float(dato[1]))
            self.datosEntrenamientoClases.append(dato[2])
        self.getConjuntoDeClases()
    def datosDeTest(self,porcentajeEntrenamiento):
        self.datosTest = self.datos[(int((self.numfilas*porcentajeEntrenamiento)/100)):]
        self.datosTestX = list()
        self.datosTestY = list()
        self.datosTestClases = list()
        for dato in self.datosTest:
            dato[0] = float(dato[0])
            dato[1] = float(dato[1])
        for dato in self.datosTest:
            self.datosTestX.append(float(dato[0]))
            self.datosTestY.append(float(dato[1]))
            self.datosTestClases.append(dato[2])
    def getConjuntoDeClases(self):
        self.conjuntoDeClases = list(dict.fromkeys(self.clases))
        return self.conjuntoDeClases
    def datos(self):
        return self.datos