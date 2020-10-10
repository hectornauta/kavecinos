
class Datos():
    def __init__(self):
        self.datosCompletos = list()
        self.clases = list()
        self.puntos = list()

        self.datosEntrenamiento = list()
        self.datosTest = list()
        self.x = list()
        self.y = list()
    def generar(self, arreglo_original):
        for dato in arreglo_original:
            self.datosCompletos.append(dato)
        for dato in self.datosCompletos:
            dato[0] = float(dato[0])
            dato[1] = float(dato[1])
            self.x.append(float(dato[0]))
            self.y.append(float(dato[1]))
        for dato in self.datosCompletos:
            self.clases.append(dato[2])
        self.clases = list(dict.fromkeys(self.clases))
    def minX(self):
        return(min(self.x))
    def maxX(self):
        return(max(self.x))
    def minY(self):
        return(min(self.y))
    def maxY(self):
        return(max(self.y))
