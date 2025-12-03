import sys
# Importamos PySide6.QtCore con un alias para una referencia más limpia
import PySide6.QtCore as QtCore 
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QTableView, QHeaderView, QMessageBox, QStyle, QStyleOption
)
from PySide6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex 
)
from PySide6.QtGui import QFont, QIcon, QPainter, QColor

from funcionesAuxiliares import crear_titulo_util, crear_encabezado_util

#Clase formulario de prestamos
class Prestamos(QWidget):
    def __init__(self):
        super().__init__()

        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.addWidget(crear_titulo_util("Gestión de Préstamos"))

        #Tabla de prestamos
        self.layout_principal.addWidget(self._crear_formualrio_prestamos())

    def _crear_formualrio_prestamos(self):
        group_widget = QWidget()
        group_widget.setMaximumHeight(150)
        layout = QGridLayout(group_widget)

        #Campos del formulario
        campos = [
            ("ID Libro:", QLineEdit()),
            ("Bibliotecario:", QComboBox()),
            ("Usuario | DNI:", QLineEdit()),
            ("Fecha devolucion estimada:", QLineEdit(placeholderText="DD/MM/AAAA"))
        ]

        #Configuracion de combobox
        campos[1][1].addItems(["Cristina", "Lorena", "Natalia", "David", "Otro"])


        #Usabilidad: Agrupar campos en Grid
        layout.addWidget(crear_encabezado_util("Registrar nuevo préstamo:"), 0, 0 , 1, 4)

        columna = 0

        for nombre, control in campos:
            label = QLabel(nombre)
            label.setBuddy(control)

            if nombre == "ID Libro:": label.setText("&ID Libro:") #Alt + I

            layout.addWidget(label,1, columna) 
            layout.addWidget(control, 2, columna)
            columna += 1        


        #Boton de accion al final de la fila de los campos
        btn_registrar = QPushButton("Registrar préstamo")
        btn_registrar.setIcon(QIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton)))
        layout.addWidget(btn_registrar, 2, columna)

        return group_widget

    def _crear_tabla_prestamos(self):
        pass