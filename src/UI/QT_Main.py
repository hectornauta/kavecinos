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

from copy import deepcopy


from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTableWidgetItem

from matplotlib import pyplot
from matplotlib import colors
import matplotlib.patches as mpatches

from QT_Main_UI import *

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


        fecha = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        self.colores = list()
        self.numero_de_divisiones = 10 #El video mostraba ~68

        self.label_2.setText(fecha)

        self.abrirDataset.clicked.connect(self.abrirArchivo)
        self.btnVerDataset.clicked.connect(self.graficarDataset)

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
    def graficarDataset(self):
        #logging.debug(archivo.x)
        #print(self.datos.datosCompletos)
        valorDeSeparacion = 1
        pyplot.clf()
        #grafico,ax = pyplot.subplots()
        grafico = pyplot.figure(figsize=(8,8))
        self.colores = colors.TABLEAU_COLORS #10 colores de momento
        
        divisionX = (self.datos.maxX() + valorDeSeparacion - self.datos.minX() + valorDeSeparacion) / (self.numero_de_divisiones)
        divisionY = (self.datos.maxY() + valorDeSeparacion - self.datos.minY() + valorDeSeparacion) / (self.numero_de_divisiones)
        #print(divisionX)
        pyplot.xlim(self.datos.minX() - valorDeSeparacion,self.datos.maxX() + valorDeSeparacion)
        pyplot.ylim(self.datos.minY() - valorDeSeparacion,self.datos.maxY() + valorDeSeparacion)

        for i in range(self.numero_de_divisiones + 1):
            pyplot.axvline(x = self.datos.minX() - valorDeSeparacion + divisionX * i)
            pyplot.axhline(y = self.datos.minY() - valorDeSeparacion + divisionY * i)

        diccionario = {}
        i = 0
        lista = list(self.colores.items())
        for clase in self.datos.clases:
            diccionario[clase] = lista[i][0]#.replace('tab:','')
            i = i + 1
        for punto in self.datos.datosCompletos:
            #print(diccionario[punto[2]])
            pyplot.plot(punto[0],punto[1],marker = 'o',color = diccionario[punto[2]])
        #pyplot.grid()

        #Crear cuadrados
        k = 7
        coordenadas = list()
        cuadrados = []
        origenX = self.datos.minX() - valorDeSeparacion
        origenY = self.datos.minY() - valorDeSeparacion
        salto = divisionX/2
        saltoDelCuadrado = divisionX
        x = origenX + salto
        y = origenX + salto
        xDelCuadrado = origenX
        yDelCuadrado = origenY
        random.seed(0)
        ax = grafico.add_subplot()
        ax.plot([origenX,divisionX*self.numero_de_divisiones],[origenY,divisionY*self.numero_de_divisiones])    
        for i in range(self.numero_de_divisiones):
            x = origenX
            xDelCuadrado = origenX
            for j in range(self.numero_de_divisiones):
                if ((random.randint(0,5))==0):
                    color = 'b'
                else:
                    color = 'g'
                cuadrado = mpatches.Rectangle((x,y),saltoDelCuadrado,saltoDelCuadrado,angle = 0.0,color=color, alpha=0.5)
                #grafico.patches.extend([pyplot.Rectangle((x,y),saltoDelCuadrado,saltoDelCuadrado,
                                  #fill=True, color=color, alpha=0.5, zorder=1000,
                                  #transform=grafico.transFigure, figure=grafico)])
                cuadrados.append(cuadrado)
                ax.add_patch(cuadrado)
                x = x + saltoDelCuadrado
                xDelCuadrado = xDelCuadrado + saltoDelCuadrado
            y = y + saltoDelCuadrado
            yDelCuadrado = yDelCuadrado + saltoDelCuadrado
        for c in cuadrados:
            print(str(c) + "/n")
        grafico.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
