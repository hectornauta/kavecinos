from QT_Main_UI import *
from PyQt5.QtWidgets import QFileDialog

import datetime


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        fecha = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.label_2.setText(fecha)

        self.abrirDataset.clicked.connect(self.abrirArchivo)


    def abrirArchivo(self):
        options = QFileDialog.Options()
        archivo, _ = QFileDialog.getOpenFileName(self, "Abrir Dataset", "",
                                                 "Archivos de texto (*.txt);; Archivos CSV (*.CSV)", options=options)
        if archivo:
            self.label_2.setText("Archivo abierto")
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()