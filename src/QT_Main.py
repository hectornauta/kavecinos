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
from core import predecirClaseConCalidad
from core import masFrecuente

from copy import deepcopy

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox

from matplotlib import pyplot
from matplotlib import colors
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

from QT_Grids import *
from QT_Main_UI import *

import random
from math import sqrt
from math import trunc
from collections import Counter

from hilos import Worker
from hilos import WorkerSignals

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QRunnable, QThreadPool,pyqtSlot, pyqtSignal
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *

import time

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        #Inicializando botones y esas weas
        self.threadpool = QThreadPool()
        
        self.txtTest.setReadOnly(True)
        self.txtMejorK.setReadOnly(True)
        self.lineElementos.setReadOnly(True)
        self.lineClases.setReadOnly(True)
        self.labelTest_2.setText(str(30))
        self.spinEntrenamiento.setValue(70)
        self.spinKUsuario.setValue(10)
        self.groupBox.setEnabled(False)
        self.radioCuadrado.setChecked(True)
        self.radioElbow.setChecked(True)
        self.barraProgreso.setEnabled(False)
        self.btnGraficoMetodo.setEnabled(False)
        self.checkRejilla.setChecked(True)
        self.checkRA.setChecked(True)
        self.checkCelda.setChecked(False)
        self.lineCelda.setEnabled(False)
        self.linePuntoX.setText('0')
        self.linePuntoY.setText('0')
        self.lineCelda.setText('0.5')
        self.btnComparacion.setEnabled(False)
        self.btnComparacion.setText('Debe calcular un K óptimo para comparar gráficos')
        self.lblCargaTexto.hide()

        rx = QRegExp("[0-9]\.?[0-9]*")
        validator = QRegExpValidator(rx, self)
        self.lineCelda.setValidator(validator)

        
        rx2 = QRegExp("[+-]?[0-9]*\.[0-9]*")
        validator2 = QRegExpValidator(rx2, self)
        self.linePuntoX.setValidator(validator2)
        self.linePuntoY.setValidator(validator2)

        
        self.comboSeparador.addItems([';',',','Tab','Espacio'])

        self.separadores = {',':',',';':';','Tab':'\t','Espacio':' '}

        self.porcentajeEntrenamiento = 70
        self.porcentajeTest = 30

        self.diccionario = {}
        self.datos = None
        self.resultadosTestMetodo = list()
        self.resultadosTestUsuario = list()

        #fecha = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        self.colores = list()
        self.ladoDeUnCuadrado = 0.5
        self.numero_de_divisiones = 70 #El video mostraba ~68
        self.kRaiz = 1
        self.kMetodo = 1
        self.laRaiz = False
        self.elMetodo = True

        self.label_2.setText('No se ha seleccionado ningún archivo')

        self.abrirDataset.clicked.connect(self.abrirArchivo)

        self.btnTestUsuario.clicked.connect(self.testearModeloUsuario)
        self.btnGraficoUsuario.clicked.connect(self.graficarUsuario)
        self.btnTestMetodo.clicked.connect(self.testearModeloMetodo)
        self.btnGraficoMetodo.clicked.connect(self.graficarMetodo)

        self.btnPredecirPunto.clicked.connect(self.predecirPunto)
        
        self.spinEntrenamiento.valueChanged.connect(self.cambiarPorcentajes)
        self.radioRaiz.toggled.connect(self.activarRaiz)
        self.radioElbow.toggled.connect(self.activarMetodo)
        self.checkCelda.stateChanged.connect(self.verCelda)
        
        self.btnComparacion.clicked.connect(self.realizarComparacion)
        
        
    def verCelda(self):
        self.lineCelda.setEnabled(self.checkCelda.isChecked())
        if self.checkCelda.isChecked():
            self.lineCelda.setText("0.5")
        
    def activarMetodo(self):
        self.laRaiz = False
        self.elMetodo = True
    def activarRaiz(self):
        self.laRaiz = True
        self.elMetodo = False
    def progress_fn(self,n):
        self.barraProgreso.setValue(n)
    def execute_this_fn(self, progress_callback):
        for n in range(0, 5):
            time.sleep(1)
            progress_callback.emit(n*100/4)
            
        return "Done."
    def print_output(self, s):
        print('')
        
    def finTestMetodo(self):
        for resultado in self.resultadosTestMetodo:
            self.txtMejorK.insertPlainText("Con K = " + str(resultado[0]) + ", la eficacia fue de " + "{:.2f}".format(resultado[1]) + "% \n")
    def finTestUsuario(self):
        for resultado in self.resultadosTestUsuario:
            self.txtTest.insertPlainText("Con K = " + str(resultado[0]) + ", la eficacia fue de " + "{:.2f}".format(resultado[1]) + "% \n")

    #☺def recurring_timer(self):
        #self.counter +=1
        #self.l.setText("Counter: %d" % self.counter)

    def hiloTestearModeloMetodo(self,progress_callback):

        self.resultadosTestMetodo = list()
        aciertos = 0
        totalElementos = 0
        totalDeTests = 10
        if self.laRaiz:
            k = self.kRaiz
        else:
            k = self.kMetodo
        total = len(self.datos.obtenerDatosTest(self.porcentajeEntrenamiento))*totalDeTests
        for i in range(1,totalDeTests+1):
            self.datos.aleatorizar()
            puntosDeEntrenamiento = self.datos.obtenerDatosEntrenamiento(self.porcentajeEntrenamiento)
            puntosDeTest = self.datos.obtenerDatosTest(self.porcentajeEntrenamiento)

            for puntoDeTest in puntosDeTest:
                loskvecinos = vecinos(puntosDeEntrenamiento,puntoDeTest,k)
                claseDelPunto = prediccion (puntoDeTest,loskvecinos)
                totalElementos = totalElementos + 1
                if (claseDelPunto==puntoDeTest[-1]):
                    aciertos = aciertos + 1
                progreso = totalElementos
                n = int((progreso*100)/total)
                progress_callback.emit(n)
        porcentajeDeAciertos = (aciertos / totalElementos) * 100
        self.resultadosTestMetodo.append((k,porcentajeDeAciertos))
    
    def testearModeloMetodo(self):
        self.txtMejorK.clear()
        self.barraProgreso.setValue(0)
        if self.laRaiz:
            self.kRaiz = self.calcularKRaiz()
            self.continuar()
        else:
            worker1 = Worker(self.hiloCalcularKElbow) # Any other args, kwargs are passed to the run function
            worker1.signals.result.connect(self.print_output)
            worker1.signals.finished.connect(self.finCalcularKElbow)
            worker1.signals.finished.connect(self.continuar)
            worker1.signals.progress.connect(self.progresoCalcularKElbow)
            self.threadpool.start(worker1)
    def continuar(self):
        self.btnGraficoMetodo.setEnabled(True)
        self.btnComparacion.setEnabled(True)
        self.btnComparacion.setText('Comparar gráficos')
        worker = Worker(self.hiloTestearModeloMetodo) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.finTestMetodo)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker) 
    def hiloTestearModeloUsuario(self,progress_callback):

        self.resultadosTestUsuario = list()
        k = self.obtenerValorDeK()
        total = k*10*len(self.datos.obtenerDatosTest(self.porcentajeEntrenamiento))
        progreso = 0
        for i in range(1,k + 1):
            aciertos = 0
            totalElementos = 0
            for j in range(1,11):
                self.datos.aleatorizar()
                puntosDeEntrenamiento =  self.datos.obtenerDatosEntrenamiento(self.porcentajeEntrenamiento)
                puntosDeTest = self.datos.obtenerDatosTest(self.porcentajeEntrenamiento)
                for puntoDeTest in puntosDeTest:
                    progreso = progreso + 1
                    loskvecinos = vecinos(puntosDeEntrenamiento,puntoDeTest,i)
                    claseDelPunto = prediccion (puntoDeTest,loskvecinos)
                    totalElementos = totalElementos + 1
                    if (claseDelPunto==puntoDeTest[-1]):
                        aciertos = aciertos + 1
                    n = int((progreso*100)/total)
                    progress_callback.emit(n)
            porcentajeDeAciertos = (aciertos / totalElementos) * 100
            self.resultadosTestUsuario.append((i,porcentajeDeAciertos))
        #for resultado in resultados:
            #self.txtTest.insertPlainText("Con K = " + str(resultado[0]) + ", la eficacia fue de " + "{:.2f}".format(resultado[1]) + "% \n")
            #TODO: esto no debería pasar porque están en hilos distintos
        #self.archivo.datosDeEntrenamiento(self.porcentajeEntrenamiento)
        #pyplot.plot(self.archivo.datosEntrenamientoX,self.archivo.datosEntrenamientoY,'go')
        #pyplot.show()
    def testearModeloUsuario(self):
        self.txtTest.clear()
        self.barraProgreso.setValue(0)
        worker = Worker(self.hiloTestearModeloUsuario) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.finTestUsuario)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)  
    
    def hayUnNumero(self):
        try:
            float(self.linePuntoX.text())
            float(self.linePuntoY.text())
            return True
        except ValueError:
            return False
    def mostrarError(self,tipo,titulo,mensaje,detalles):
        coso = QMessageBox()
        if tipo=='Critical':
            coso.setIcon(QMessageBox.Critical)
        else:
            if tipo=='Information':
                coso.setIcon(QMessageBox.Information)   
        coso.setText(mensaje)
        coso.setInformativeText('')
        coso.setWindowTitle(titulo)
        if detalles!='':
            coso.setDetailedText(detalles)
        coso.setStandardButtons(QMessageBox.Ok)
        #coso.buttonClicked.connect(msgbtn)
        retval = coso.exec_()
    def predecirPunto(self):
        self.txtTest.clear()
        mipunto = list()
        if self.hayUnNumero():
            mipunto.append(float(self.linePuntoX.text()))
            mipunto.append(float(self.linePuntoY.text()))
            #puntosDeEntrenamiento = self.datos.obtenerDatosEntrenamiento(self.porcentajeEntrenamiento)
            #puntosDeTest = self.datos.obtenerDatosTest(self.porcentajeEntrenamiento)
            for i in range(1,11):
                loskvecinos = vecinos(self.datos.datosCompletos,mipunto,i)
                #print("Para " + str(i) + " vecinos sus vecinos más cercanos son:")
                #print(loskvecinos)
                claseDelPunto = prediccion (mipunto,loskvecinos)
                #print("La clase predicha fue " + claseDelPunto)
                self.txtTest.insertPlainText("Con " +str(i) + " vecinos, la clase predicha fue " + claseDelPunto + "\n")
            #self.archivo.datosDeEntrenamiento(self.porcentajeEntrenamiento)
            #pyplot.plot(self.archivo.datosEntrenamientoX,self.archivo.datosEntrenamientoY,'go')
            #pyplot.show()      
        else:
            tipo='Critical'
            titulo = 'Error'
            mensaje = 'No has ingresado un punto válido'
            detalles = 'Las coordenadas ingresadas no son válidas'
            self.mostrarError(tipo,titulo,mensaje,detalles)
    def cambiarPorcentajes(self):
        self.porcentajeEntrenamiento = self.spinEntrenamiento.value()
        self.porcentajeTest = 100 - self.spinEntrenamiento.value()
        self.labelTest_2.setText(str(self.porcentajeTest))
        self.btnGraficoMetodo.setEnabled(False)
        self.btnComparacion.setEnabled(False)
        self.btnComparacion.setText('Debe calcular un K óptimo para comparar gráficos')

    def cambiarKUsuario(self):
        self.valorDeK = self.spinKUsuario.value()

    def abrirArchivo(self):
        options = QFileDialog.Options()
        ruta_de_archivo, _ = QFileDialog.getOpenFileName(self, "Abrir Dataset", "",
                                                 "Archivos de texto (*.txt);; Archivos CSV (*.CSV)", options=options)
        if ruta_de_archivo:
            self.label_2.setText(ruta_de_archivo)
            self.archivo = Archivo(ruta_de_archivo)
            self.archivo.abrir(self.separadores[self.comboSeparador.currentText()])
            self.groupBox.setEnabled(True)
            self.barraProgreso.setEnabled(True)
            self.txtTest.clear()
            self.txtMejorK.clear()

            self.valorDeK = 7

            #print("datos del archivo")
            #print(self.archivo.datos)
            self.datos = Datos()
            self.datos.atributos = self.archivo.columnas
            self.datos.generar(deepcopy(self.archivo.datos))

            #print("datos del archivo")
            #print(self.archivo.datos)

            self.tableWidget.setColumnCount(self.archivo.numcolumnas)
            self.tableWidget.setRowCount(self.archivo.numfilas)
            self.tableWidget.setHorizontalHeaderLabels(self.archivo.columnas)
            self.lineClases.setText(str(self.datos.obtenerNumeroDeClases()))
            self.lineElementos.setText(str(self.datos.obtenerCantidad()))

            
            for fila in range(self.archivo.numfilas):
                for columna in range(self.archivo.numcolumnas):
                    self.tableWidget.setItem(fila, columna, QTableWidgetItem((self.archivo.datos[fila][columna])))

        else:
            self.label_2.setText("No se ha seleccionado ningún archivo")
            self.groupBox.setEnabled(False)
            self.barraProgreso.setEnabled(False)
    def obtenerValorDeK(self):
        return int(self.spinKUsuario.value())
    def obtenerMejorK(self):
        if (self.radioRaiz.isChecked()):
            return self.calcularKRaiz()
        else:
            return self.calcularKElbow()

    def calcularKRaiz(self):
        k = int(sqrt(self.datos.obtenerCantidad()))
        if (((k % 2) == 0) and (((self.datos.obtenerNumeroDeClases())%2)==0)):
            k = k + 1
        return k

    def finCalcularKElbow(self):
        self.txtMejorK.insertPlainText("Se ha detectado un k óptimo igual a " + str(self.kMetodo) + "\n ------------- \n")
    def progresoCalcularKElbow(self,n):
        self.txtMejorK.insertPlainText('Analizando K = ' + str(n) + "\n")
    def hiloCalcularKElbow(self,progress_callback):
        puntosDeEntrenamiento = self.datos.obtenerDatosEntrenamiento(self.porcentajeEntrenamiento)
        puntosDeTest = self.datos.obtenerDatosTest(self.porcentajeEntrenamiento)
        raiz = self.calcularKRaiz()
        self.resultadosTestMetodo = list()
        aciertos = 0
        totalElementos = 0
        k = 1
        mejorK = 1
        fin = False
        mejorValor = 0
        j = 0

        while (not fin):
            progress_callback.emit(k)
            aciertos = 0
            totalElementos = 0
            for puntoDeTest in puntosDeTest:
                loskvecinos = vecinos(puntosDeEntrenamiento,puntoDeTest,k)
                claseDelPunto = prediccion (puntoDeTest,loskvecinos)
                totalElementos = totalElementos + 1
                if (claseDelPunto==puntoDeTest[-1]):
                    aciertos = aciertos + 1
            porcentajeDeAciertos = (aciertos / totalElementos) * 100
            self.resultadosTestMetodo.append((k,porcentajeDeAciertos))
            #¹print('k' + str(k) + 'j' + str(j) + 'raiz' + str(raiz))
            if (porcentajeDeAciertos>mejorValor):
                mejorValor = porcentajeDeAciertos
                mejorK = k
                j = 0
            else:
                j = j + 1
            if ((j>(raiz/2)) or (k>raiz)):
                fin = True
            else:
                k = k + 1    
        #for resultado in resultados:
            #self.txtMejorK.insertPlainText("Con K = " + str(resultado[0]) + ", la eficacia fue de " + "{:.2f}".format(resultado[1]) + "% \n")
        self.kMetodo = mejorK
    def obtenerRejilla(self):
        return (self.checkRejilla.isChecked())
    def obtenerRA(self):
        if self.checkRA.isChecked():
            return True
        else:
            return False
        return (self.checkRejilla.isChecked())
    def obtenerCelda(self):
        if (self.checkCelda.isChecked() and (0<float(self.lineCelda.text()))):
            return float(self.lineCelda.text())
        else:
            return 0.5
    def insertarGrid(self,grafico,ejes,limiteInferiorX,limiteSuperiorX,limiteInferiorY,limiteSuperiorY,k,salto):
        #¶coordenadas = list()
        cuadrados = []
        x = limiteInferiorX
        y = limiteInferiorY

        xDePrueba = x + salto/2
        yDePrueba = y + salto/2
        while(y<limiteSuperiorY):
            x = limiteInferiorX
            xDePrueba = x + salto/2
            while(x<limiteSuperiorX):
                clase = predecirClase(self.datos.datosCompletos,(xDePrueba,yDePrueba),k)
                color = self.diccionario[clase]
                cuadrado = mpatches.Rectangle((x,y),salto,salto,angle = 0.0,color=color, alpha=0.4,linewidth=0)
                #grafico.patches.extend([pyplot.Rectangle((x,y),saltoDelCuadrado,saltoDelCuadrado,
                                  #fill=True, color=color, alpha=0.5, zorder=1000,
                                  #transform=grafico.transFigure, figure=grafico)])
                cuadrados.append(cuadrado)
                ejes.add_patch(cuadrado)
                x = x + salto
                xDePrueba = x + salto/2
            y = y + salto
            yDePrueba = y + salto/2
        #for c in cuadrados:
            #print(str(c) + "/n")
    def insertarCirculos(self,grafico,ejes,limiteInferiorX,limiteSuperiorX,limiteInferiorY,limiteSuperiorY,k,salto):
        cuadrados = []
        x = limiteInferiorX
        y = limiteInferiorY

        xDePrueba = x + salto/2
        yDePrueba = y + salto/2
        while(y<limiteSuperiorY):
            x = limiteInferiorX
            xDePrueba = x + salto/2
            while(x<limiteSuperiorX):
                clase = (predecirClaseConCalidad(self.datos.datosCompletos,(xDePrueba,yDePrueba),k))[0]
                calidad = (predecirClaseConCalidad(self.datos.datosCompletos,(xDePrueba,yDePrueba),k))[1]
                calidad = ((salto/2)*(calidad))
                color = self.diccionario[clase]
                cuadrado = mpatches.Circle((x+(salto/2),y+(salto/2)),radius=calidad,color=color, alpha=0.4,linewidth=0)
                #grafico.patches.extend([pyplot.Rectangle((x,y),saltoDelCuadrado,saltoDelCuadrado,
                                  #fill=True, color=color, alpha=0.5, zorder=1000,
                                  #transform=grafico.transFigure, figure=grafico)])
                cuadrados.append(cuadrado)
                ejes.add_patch(cuadrado)
                x = x + salto
                xDePrueba = x + salto/2
            y = y + salto
            yDePrueba = y + salto/2
        #for c in cuadrados:
            #print(str(c) + "/n")
    def graficarMetodo(self):
        if self.laRaiz:
            k = self.kRaiz
            mensaje = 'Raiz'
        else:
            k = self.kMetodo
            mensaje = 'Codo'
        self.graficarDataset(k,mensaje,False)
    def graficarUsuario(self):
        k = self.obtenerValorDeK()
        self.graficarDataset(k,'Usuario',False)
    def realizarComparacion(self):
        self.lblCargaTexto.show()
        tipo='Information'
        titulo = 'Aviso'
        mensaje = 'Esta operación podría tardar. Por favor espere...'
        detalles = ''
        self.mostrarError(tipo,titulo,mensaje,detalles)
        kUsuario = self.obtenerValorDeK()
        if self.laRaiz:
            kMetodo = self.kRaiz
            metodo = 'Raiz'
        else:
            kMetodo = self.kMetodo
            metodo = 'Codo'
        for k in range(1,kUsuario+1):
            self.graficarDataset(k,'Usuario',True)
        self.graficarDataset(kMetodo,metodo,True)

        self.ventanaComparacion = Grids(kUsuario,kMetodo)
        self.ventanaComparacion.show()
        self.lblCargaTexto.hide()


    def graficarDataset(self,k,tipoDeGrafico,imprimir):
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
        if self.obtenerRA():
            ax.set_aspect(1)
        if(len(self.datos.clases)>9):
            self.colores = colors.CSS4_COLORS
        else:
            self.colores = colors.TABLEAU_COLORS
        
        #divisionX = (self.datos.maxX() + valorDeSeparacionX - self.datos.minX() + valorDeSeparacionY) / (self.numero_de_divisiones)
        #divisionY = (self.datos.maxY() + valorDeSeparacionY - self.datos.minY() + valorDeSeparacionY) / (self.numero_de_divisiones)
        #print(divisionX)

        limiteCeldaX = (trunc(((limiteSuperiorX-limiteInferiorX)/self.obtenerCelda()))+1)*self.obtenerCelda()+limiteInferiorX
        limiteCeldaY = (trunc(((limiteSuperiorY-limiteInferiorY)/self.obtenerCelda()))+1)*self.obtenerCelda()+limiteInferiorY

        pyplot.xlim(limiteInferiorX,limiteCeldaX)
        pyplot.ylim(limiteInferiorY,limiteCeldaY)

        pyplot.xlabel(self.datos.atributos[0])
        pyplot.ylabel(self.datos.atributos[1])

        xDelBucle = limiteInferiorX
        yDelBucle = limiteInferiorY
        
        if(self.obtenerRejilla()):
            while(xDelBucle<limiteSuperiorX):
                pyplot.axvline(x = xDelBucle,linestyle = '-',marker = ",",linewidth=0.2)
                xDelBucle = xDelBucle + self.obtenerCelda()
            while(yDelBucle<limiteSuperiorY):
                pyplot.axhline(y = yDelBucle,linestyle = '-',marker = ",",linewidth=0.2)
                yDelBucle = yDelBucle + self.obtenerCelda()

        self.diccionario = {}
        i = 0
        lista = list(self.colores.items())
        for clase in self.datos.clases:
            self.diccionario[clase] = lista[i][0]
            i = i + 1        
        puntos = self.datos.datosCompletos#ËpuntosEntrenamiento = self.datos.obtenerDatosEntrenamiento(self.porcentajeEntrenamiento)
        for punto in puntos:#puntosEntrenamiento:
            pyplot.plot(punto[0],punto[1],marker = '.',color = self.diccionario[punto[2]])
            
        leyendas = []
        for clase in self.datos.clases:
            leyendas.append(Line2D([0],[0],lw=4,marker='o',color=self.diccionario[clase]))
        pyplot.legend(leyendas, self.datos.clases,loc='upper left')

        if (self.radioCuadrado.isChecked()==True):
            self.insertarGridV2(grafico,ax,limiteInferiorX,limiteSuperiorX,limiteInferiorY,limiteSuperiorY,k,self.obtenerCelda())
        else:
            self.insertarCirculos(grafico,ax,limiteInferiorX,limiteSuperiorX,limiteInferiorY,limiteSuperiorY,k,self.obtenerCelda())
        if tipoDeGrafico=='Usuario':
            nombre = tipoDeGrafico + str(k)
        else:
            nombre = 'Metodo'
        if tipoDeGrafico=='Raiz':
            mensaje = 'Utilizando método de la Raíz con k = '
        else:
            if tipoDeGrafico=='Codo':
                mensaje = 'Utilizando método del codo con k = '
            else:
                mensaje = 'Rango de K ingresado por el usuario, k = '
        mensaje = mensaje + str(k)
        pyplot.title(mensaje)
        
        if imprimir:
            grafico.savefig(nombre)
        else:
            grafico.show()

    def insertarGridV2(self,grafico,ejes,limiteInferiorX,limiteSuperiorX,limiteInferiorY,limiteSuperiorY,k,salto):
        cuadrados = []
        x = limiteInferiorX
        y = limiteInferiorY

        #xDePrueba = x + salto/2
        yDePrueba = y + salto/2

        while(y<limiteSuperiorY):
            x = limiteInferiorX
            xDePrueba = x + salto/2
            while(x<limiteSuperiorX):
                clases = []
                clase1 = predecirClase(self.datos.datosCompletos,(xDePrueba-(salto/2),yDePrueba-(salto/2)),k)
                clases.append(clase1)
                clase2 = predecirClase(self.datos.datosCompletos,(xDePrueba-(salto/2),yDePrueba+(salto/2)),k)
                clases.append(clase2)
                clase3 = predecirClase(self.datos.datosCompletos,(xDePrueba+(salto/2),yDePrueba-(salto/2)),k)
                clases.append(clase3)
                clase4 = predecirClase(self.datos.datosCompletos,(xDePrueba+(salto/2),yDePrueba+(salto/2)),k)
                clases.append(clase4)
                contadores = Counter(clases)
                clase = masFrecuente(clases)
                calidad = contadores[clase]
                if calidad==1:
                    proporcion=0.0
                else:
                    if calidad==2:
                        proporcion=0.1
                    else:
                        if calidad==3:
                            proporcion=0.5
                        else:
                            proporcion=1
                color = self.diccionario[clase]
                cuadrado = mpatches.Rectangle((x,y),salto,salto,angle = 0.0,color=color, alpha=(0.5*proporcion),linewidth=0)
                cuadrados.append(cuadrado)
                ejes.add_patch(cuadrado)
                x = x + salto
                xDePrueba = x + salto/2
            y = y + salto
            yDePrueba = y + salto/2   
    def insertarGridV3(self,grafico,ejes,limiteInferiorX,limiteSuperiorX,limiteInferiorY,limiteSuperiorY,k,salto):
        x = limiteInferiorX
        y = limiteInferiorY

        xDePrueba = x + salto/2
        yDePrueba = y + salto/2

        tabla = []

        while(y<limiteSuperiorY):
            x = limiteInferiorX
            xDePrueba = x + salto/2
            fila = []
            while(x<limiteSuperiorX):
                clases = []
                clase1 = predecirClase(self.datos.datosCompletos,(xDePrueba-(salto/2),yDePrueba-(salto/2)),k)
                clases.append(clase1)
                clase2 = predecirClase(self.datos.datosCompletos,(xDePrueba-(salto/2),yDePrueba+(salto/2)),k)
                clases.append(clase2)
                clase3 = predecirClase(self.datos.datosCompletos,(xDePrueba+(salto/2),yDePrueba-(salto/2)),k)
                clases.append(clase3)
                clase4 = predecirClase(self.datos.datosCompletos,(xDePrueba+(salto/2),yDePrueba+(salto/2)),k)
                clases.append(clase4)
                contadores = Counter(clases)
                clase = masFrecuente(clases)
                calidad = contadores[clase]
                if calidad==1:
                    proporcion=0.0
                else:
                    if calidad==2:
                        proporcion=0.1
                    else:
                        if calidad==3:
                            proporcion=0.5
                        else:
                            proporcion=1
                color = self.diccionario[clase]
                celda = []
                celda.append((clase,proporcion))
                fila.append(celda)
                x = x + salto
                xDePrueba = x + salto/2
            tabla.insert(0,fila)
            y = y + salto
            yDePrueba = y + salto/2      
        print(tabla)  

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
