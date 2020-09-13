# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QT_Main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 90, 781, 441))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 81, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(100, 15, 461, 31))
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_2.setObjectName("label_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 60, 311, 191))
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(340, 60, 431, 461))
        self.groupBox_3.setObjectName("groupBox_3")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_3)
        self.tableWidget.setGeometry(QtCore.QRect(10, 20, 411, 421))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.abrirDataset = QtWidgets.QPushButton(self.centralwidget)
        self.abrirDataset.setGeometry(QtCore.QRect(10, 10, 101, 41))
        self.abrirDataset.setObjectName("abrirDataset")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuProyecto = QtWidgets.QMenu(self.menubar)
        self.menuProyecto.setObjectName("menuProyecto")
        self.menuEntrenar = QtWidgets.QMenu(self.menubar)
        self.menuEntrenar.setObjectName("menuEntrenar")
        self.menuAyuda = QtWidgets.QMenu(self.menubar)
        self.menuAyuda.setObjectName("menuAyuda")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNuevo_Proyecto = QtWidgets.QAction(MainWindow)
        self.actionNuevo_Proyecto.setObjectName("actionNuevo_Proyecto")
        self.actionSalir = QtWidgets.QAction(MainWindow)
        self.actionSalir.setObjectName("actionSalir")
        self.menuProyecto.addAction(self.actionNuevo_Proyecto)
        self.menuProyecto.addSeparator()
        self.menuProyecto.addAction(self.actionSalir)
        self.menubar.addAction(self.menuProyecto.menuAction())
        self.menubar.addAction(self.menuEntrenar.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Dataset"))
        self.label.setText(_translate("MainWindow", "Ruta del dataset"))
        self.label_2.setText(_translate("MainWindow", "No se ha seleccionado ningún dataset"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Parámetros del algoritmo"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Datos"))
        self.abrirDataset.setText(_translate("MainWindow", "Abrir Dataset"))
        self.menuProyecto.setTitle(_translate("MainWindow", "Proyecto"))
        self.menuEntrenar.setTitle(_translate("MainWindow", "Entrenar"))
        self.menuAyuda.setTitle(_translate("MainWindow", "Ayuda"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionNuevo_Proyecto.setText(_translate("MainWindow", "Abrir Dataset"))
        self.actionSalir.setText(_translate("MainWindow", "Salir"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

