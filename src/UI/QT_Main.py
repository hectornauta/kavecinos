import datetime
import os
import sys
#import logging
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
from archivo import Archivo
from core import *


from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTableWidgetItem

from matplotlib import pyplot

from QT_Main_UI import *


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        fecha = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.label_2.setText(fecha)

        self.abrirDataset.clicked.connect(self.abrirArchivo)
        self.btnVerDataset.clicked.connect(self.graficarDataset)

        self.btnEntrenar.clicked.connect(self.entrenarModelo)
        self.spinEntrenamiento.valueChanged.connect(self.cambiarPorcentajes)

        #Inicializar widgets

    def entrenarModelo(self):
        archivo.datosDeEntrenamiento(self.porcentajeEntrenamiento)
        pyplot.plot(archivo.datosEntrenamientoX,archivo.datosEntrenamientoY,'go')
        pyplot.show()
        
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
            global archivo
            archivo = Archivo(ruta_de_archivo)
            archivo.abrir()

            self.tableWidget.setColumnCount(archivo.numcolumnas)
            self.tableWidget.setRowCount(archivo.numfilas)
            self.tableWidget.setHorizontalHeaderLabels(archivo.columnas)

            for fila in range(archivo.numfilas):
                for columna in range(archivo.numcolumnas):
                    self.tableWidget.setItem(fila, columna, QTableWidgetItem((archivo.datos[fila][columna])))

        else:
            self.label_2.setText("Archivo no encontrado")
    def graficarDataset(self):
        #logging.debug(archivo.x)
        print(archivo.datosEntrenamiento)
        for punto in archivo.datosEntrenamiento:
            if punto[2] == archivo.conjuntoDeClases[0]:
                pyplot.plot(punto[0],punto[1],'bo')
            else:
                pyplot.plot(punto[0],punto[1],'ro')
        #TODO: Hacer ciclo para todas categorizar todas las clases
        pyplot.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
