import datetime
import os
import sys
#import logging
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
from archivo import Archivo
from datos import Datos
from core import vecinos
from core import distancia
from core import prediccion
from core import predecirClase

from copy import deepcopy


from matplotlib import pyplot
from matplotlib import colors
import matplotlib.patches as mpatches


import random


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        #Inicializando botones y esas weas
        
        self.btnEntrenar.setEnabled(False)
        self.btnVerDataset.setEnabled(False)
        self.btnTest.setEnabled(False)
        self.txtDebug.setReadOnly(True)
        self.btnPredecirPunto.setEnabled(False)
        self.spinEntrenamiento.setEnabled(False)
        self.labelTest_2.setText(str(30))
        self.spinEntrenamiento.setValue(70)
        self.linePuntoX.setEnabled(False)
        self.linePuntoY.setEnabled(False)

        self.porcentajeEntrenamiento = 70
        self.porcentajeTest = 30

        self.diccionario = {}

        fecha = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        self.colores = list()
        self.ladoDeUnCuadrado = 1
        self.numero_de_divisiones = 70 #El video mostraba ~68

        self.label_2.setText(fecha)


        self.btnEntrenar.clicked.connect(self.entrenarModelo)
        self.btnTest.clicked.connect(self.testearModelo)
        self.btnPredecirPunto.clicked.connect(self.predecirPunto)
        self.spinEntrenamiento.valueChanged.connect(self.cambiarPorcentajes)

        #Inicializar widgets

    def entrenarModelo(self):
        self.archivo.datosDeEntrenamiento(self.porcentajeEntrenamiento)
        pyplot.plot(self.archivo.datosEntrenamientoX,self.archivo.datosEntrenamientoY,'go')
        pyplot.show()
        #TODO: actualizar con los nuevos datos
    def predecirPunto(self):
        #mipunto = [5.91,3.79]

        mipunto = list()
        mipunto.append(float(self.linePuntoX.text()))
        mipunto.append(float(self.linePuntoY.text()))
        
        self.datos.aleatorizar()
        #puntosDeEntrenamiento = self.datos.obtenerDatosEntrenamiento(self.porcentajeEntrenamiento)
        #puntosDeTest = self.datos.obtenerDatosTest(self.porcentajeEntrenamiento)
        for i in range(1,11):
            loskvecinos = vecinos(self.datos.datosCompletos,mipunto,i)
            #print("Para " + str(i) + " vecinos sus vecinos más cercanos son:")
            #print(loskvecinos)
            claseDelPunto = prediccion (mipunto,loskvecinos)
            #print("La clase predicha fue " + claseDelPunto)
            self.txtDebug.insertPlainText("Con " +str(i) + " vecinos, la clase predicha fue " + claseDelPunto + "\n")
        #self.archivo.datosDeEntrenamiento(self.porcentajeEntrenamiento)
        #pyplot.plot(self.archivo.datosEntrenamientoX,self.archivo.datosEntrenamientoY,'go')
        #pyplot.show()
    def testearModelo(self):
        self.txtDebug.clear()
        self.datos.aleatorizar()
        print(self.datos.datosCompletos)
        puntosDeEntrenamiento = self.datos.obtenerDatosEntrenamiento(self.porcentajeEntrenamiento)
        puntosDeTest = self.datos.obtenerDatosTest(self.porcentajeEntrenamiento)

        resultados = list()

        for i in range(1,11):
            aciertos = 0
            totalElementos = 0
            #TODO: mostrar en una tabla los resultados, por ejemplo
            #clasesPredichas = list()
            #clasesReales = list()
            for puntoDeTest in puntosDeTest:
                loskvecinos = vecinos(puntosDeEntrenamiento,puntoDeTest,i)
                claseDelPunto = prediccion (puntoDeTest,loskvecinos)
                totalElementos = totalElementos + 1
                if (claseDelPunto==puntoDeTest[-1]):
                    aciertos = aciertos + 1
            porcentajeDeAciertos = (aciertos / totalElementos) * 100
            resultados.append((i,porcentajeDeAciertos))
        for resultado in resultados:
            self.txtDebug.insertPlainText("Para un k = " + str(resultado[0]) + " el porcentaje de aciertos fue de " + "{:.2f}".format(resultado[1]) + "% \n")
        #self.archivo.datosDeEntrenamiento(self.porcentajeEntrenamiento)
        #pyplot.plot(self.archivo.datosEntrenamientoX,self.archivo.datosEntrenamientoY,'go')
        #pyplot.show()
        
    def cambiarPorcentajes(self):
        self.porcentajeEntrenamiento = self.spinEntrenamiento.value()
        self.porcentajeTest = 100 - self.spinEntrenamiento.value()
        self.labelTest_2.setText(str(self.porcentajeTest))

    def abrirArchivo(self):
        options = QFileDialog.Options()
        ruta_de_archivo, _ = QFileDialog.getOpenFileName(self, "Abrir Dataset", "",
                                                 "Archivos de texto (*.txt);; Archivos CSV (*.CSV)", options=options)
        if ruta_de_archivo:
            self.label_2.setText(ruta_de_archivo)
            self.archivo = Archivo(ruta_de_archivo)
            self.archivo.abrir()
            self.btnVerDataset.setEnabled(True)
            self.btnTest.setEnabled(True)
            self.btnPredecirPunto.setEnabled(True)
            self.spinEntrenamiento.setEnabled(True)
            self.linePuntoX.setEnabled(True)
            self.linePuntoY.setEnabled(True)

            #print("datos del archivo")
            #print(self.archivo.datos)
            self.datos = Datos()

            self.datos.generar(deepcopy(self.archivo.datos))

            #print("datos del archivo")
            #print(self.archivo.datos)

            self.tableWidget.setColumnCount(self.archivo.numcolumnas)
            self.tableWidget.setRowCount(self.archivo.numfilas)
            self.tableWidget.setHorizontalHeaderLabels(self.archivo.columnas)

            
            for fila in range(self.archivo.numfilas):
                for columna in range(self.archivo.numcolumnas):
                    self.tableWidget.setItem(fila, columna, QTableWidgetItem((self.archivo.datos[fila][columna])))

        else:
            self.label_2.setText("Archivo no encontrado")

    def insertarGrid(self,grafico,ejes,limiteInferiorX,limiteSuperiorX,limiteInferiorY,limiteSuperiorY,k,salto):
        coordenadas = list()
        cuadrados = []
        x = limiteInferiorX
        y = limiteInferiorY
        random.seed(datetime.datetime.now())

        xDePrueba = x + self.ladoDeUnCuadrado/2
        yDePrueba = y + self.ladoDeUnCuadrado/2
        while(y<limiteSuperiorY):
            x = limiteInferiorX
            xDePrueba = x + self.ladoDeUnCuadrado/2
            while(x<limiteSuperiorX):
                clase = predecirClase(self.datos.datosCompletos,(xDePrueba,yDePrueba),k)
                color = self.diccionario[clase]
                cuadrado = mpatches.Rectangle((x,y),self.ladoDeUnCuadrado,self.ladoDeUnCuadrado,angle = 0.0,color=color, alpha=0.5)
                #grafico.patches.extend([pyplot.Rectangle((x,y),saltoDelCuadrado,saltoDelCuadrado,
                                  #fill=True, color=color, alpha=0.5, zorder=1000,
                                  #transform=grafico.transFigure, figure=grafico)])
                cuadrados.append(cuadrado)
                ejes.add_patch(cuadrado)
                x = x + self.ladoDeUnCuadrado
                xDePrueba = x + self.ladoDeUnCuadrado/2
            y = y + self.ladoDeUnCuadrado
            yDePrueba = y + self.ladoDeUnCuadrado/2
        #for c in cuadrados:
            #print(str(c) + "/n")
    def graficarDataset(self):
        valorDeSeparacionX = (self.datos.maxX()-self.datos.minX())*0.1
        valorDeSeparacionY = (self.datos.maxY()-self.datos.minY())*0.1
        limiteInferiorX = self.datos.minX() - valorDeSeparacionX
        limiteSuperiorX =self.datos.maxX() + valorDeSeparacionX
        limiteInferiorY = self.datos.minY() - valorDeSeparacionY
        limiteSuperiorY =self.datos.maxY() + valorDeSeparacionY
        pyplot.clf()
        grafico = pyplot.figure(figsize=(8,8))
        ax = grafico.add_subplot()
        ax.plot(limiteInferiorX,limiteInferiorY)
        ax.set_aspect(1)
        self.colores = colors.TABLEAU_COLORS #10 colores de momento
        
        #divisionX = (self.datos.maxX() + valorDeSeparacionX - self.datos.minX() + valorDeSeparacionY) / (self.numero_de_divisiones)
        #divisionY = (self.datos.maxY() + valorDeSeparacionY - self.datos.minY() + valorDeSeparacionY) / (self.numero_de_divisiones)
        #print(divisionX)
        pyplot.xlim(limiteInferiorX,limiteSuperiorX)
        pyplot.ylim(limiteInferiorY,limiteSuperiorY)

        xDelBucle = limiteInferiorX
        yDelBucle = limiteInferiorY
        while(xDelBucle<limiteSuperiorX):
            pyplot.axvline(x = xDelBucle,linestyle = '-',marker = ",",linewidth=0.5)
            xDelBucle = xDelBucle + self.ladoDeUnCuadrado
        while(yDelBucle<limiteSuperiorY):
            pyplot.axhline(y = yDelBucle,linestyle = '-',marker = ",",linewidth=0.5)
            yDelBucle = yDelBucle + self.ladoDeUnCuadrado

        self.diccionario = {}
        i = 0
        lista = list(self.colores.items())
        for clase in self.datos.clases:
            self.diccionario[clase] = lista[i][0]
            i = i + 1
        for punto in self.datos.datosCompletos:
            pyplot.plot(punto[0],punto[1],marker = '.',color = self.diccionario[punto[2]])
        k = 7
        self.insertarGrid(grafico,ax,limiteInferiorX,limiteSuperiorX,limiteInferiorY,limiteSuperiorY,k,self.ladoDeUnCuadrado)
        #Crear cuadrados
        
        grafico.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
