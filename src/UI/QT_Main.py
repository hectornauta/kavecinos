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

from QT_Main_UI import *


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


        fecha = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        self.datos = Datos()
        self.colores = list()
        self.numero_de_divisiones = 10

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
        #mipunto = [5.91,3.79]

        mipunto = list()
        mipunto.append(float(self.txtPuntoX.toPlainText()))
        mipunto.append(float(self.txtPuntoY.toPlainText()))
        
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
            #self.btnTest.setEnabled(True)
            self.btnPredecirPunto.setEnabled(True)
            self.spinEntrenamiento.setEnabled(True)
            self.linePuntoX.setEnabled(True)
            self.linePuntoY.setEnabled(True)

            #print("datos del archivo")
            #print(self.archivo.datos)

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

        self.colores = colors.TABLEAU_COLORS
        
        divisionX = (self.datos.maxX() + 1 - self.datos.minX() + 1) / (self.numero_de_divisiones)
        divisionY = (self.datos.maxY() + 1 - self.datos.minY() + 1) / (self.numero_de_divisiones)
        #print(divisionX)

        pyplot.xlim(self.datos.minX() - 1,self.datos.maxX() + 1)
        pyplot.ylim(self.datos.minY() - 1,self.datos.maxY() + 1)

        for i in range(self.numero_de_divisiones + 1):
            pyplot.axvline(x = self.datos.minX() - 1 + divisionX * i)
            pyplot.axhline(y = self.datos.minY() - 1 + divisionY * i)

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
        pyplot.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
