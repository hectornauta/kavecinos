from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtGui
from QT_Grids_UI import Ui_Form

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap

class Grids(QMainWindow):

    def __init__(self,k):
        super().__init__()
        self.ventana = Ui_Form()
        self.ventana.setupUi(self)

        self.ventana.btnAnt.setEnabled(False)
        if k==1:
            self.ventana.btnProx.setEnabled(False)
        self.kActual = 1
        self.kMaximo = k

        self.ventana.lblUsuario.setPixmap(QPixmap('Usuario'+str(1)+'.png'))
        self.ventana.lblMetodo.setPixmap(QPixmap('Metodo.png'))

        self.ventana.btnAnt.clicked.connect(self.atras)
        self.ventana.btnProx.clicked.connect(self.adelante)
    def atras(self):
        self.kActual=self.kActual-1
        self.ventana.lblUsuario.setPixmap(QPixmap('Usuario'+str(self.kActual)+'.png'))
        if self.kActual==1:
            self.ventana.btnAnt.setEnabled(False)
        if self.kActual!=self.kMaximo:
            self.ventana.btnProx.setEnabled(True)

    def adelante(self):
        self.kActual=self.kActual+1
        self.ventana.lblUsuario.setPixmap(QPixmap('Usuario'+str(self.kActual)+'.png'))
        if self.kActual!=1:
            self.ventana.btnAnt.setEnabled(True)
        if self.kActual==self.kMaximo:
            self.ventana.btnProx.setEnabled(False)