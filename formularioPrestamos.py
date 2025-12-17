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
from biblioteca import TableModel as BibliotecaTableModel

import datos

# Clase formulario de prestamos
class Prestamos(QWidget):
    def __init__(self):
        super().__init__()

        self.layout_principal = QVBoxLayout(self)
        # Layout contenedor
        self.layout_contenedor = QHBoxLayout()
        self.layout_principal.addWidget(crear_titulo_util("Gestión de Préstamos"))

        # Formulario de prestamos
        self.layout_principal.addWidget(self._crear_formulario_prestamos())
        # Tabla de prestamos
        self.layout_contenedor.addWidget(self._crear_tabla_prestamos())
        
        self.layout_principal.addLayout(self.layout_contenedor)

    def _crear_formulario_prestamos(self):
        group_widget = QWidget()
        group_widget.setMaximumHeight(150)
        layout = QGridLayout(group_widget)

        # Campos del formulario
        campos = [
            ("ID Libro:", QLineEdit()),
            ("Bibliotecario:", QComboBox()),
            ("Usuario | DNI:", QLineEdit()),
            ("Fecha devolucion estimada:", QLineEdit(placeholderText="DD/MM/AAAA"))
        ]

        # Configuracion de combobox
        campos[1][1].addItems(["Cristina", "Lorena", "Natalia", "David", "Otro"])


        # Usabilidad: Agrupar campos en Grid
        layout.addWidget(crear_encabezado_util("Registrar nuevo préstamo:"), 0, 0, 1, 4)

        columna = 0

        for nombre, control in campos:
            label = QLabel(nombre)
            label.setBuddy(control)

            if nombre == "ID Libro:": label.setText("&ID Libro:") #Alt + I

            layout.addWidget(label,1, columna) 
            layout.addWidget(control, 2, columna)
            columna += 1        


        # Boton de accion al final de la fila de los campos
        btn_registrar = QPushButton("Registrar préstamo")
        btn_registrar.setIcon(QIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton)))
        layout.addWidget(btn_registrar, 2, columna)

        return group_widget

    def _crear_tabla_prestamos(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        cabecera = ["ID Préstamo", "Libro", "Usuario", "Fecha Préstamo", "Fecha Devolución Estimada", "Estado"]
        self.modelo_libros = BibliotecaTableModel(datos.PRESTAMOS, cabecera)
        
        self.tabla_libros = QTableView()
        self.tabla_libros.setModel(self.modelo_libros)
        
        header = self.tabla_libros.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents) #Para no usar scroll horizontal
        header.setStretchLastSection(True) # La ultima columna ocupa espacio restante
        
        self.tabla_libros.setSelectionBehavior(QTableView.SelectRows) # Seleccionar fila completa
        self.tabla_libros.setEditTriggers(QTableView.NoEditTriggers) # No permite ediciones
        
        #Añadimos los widget
        layout.addWidget(crear_encabezado_util("Catálogo de Libros - Biblioteca"))
        layout.addWidget(self.tabla_libros)
        
        #Creamos el layout de botones con sus botones
        layout_botones = QHBoxLayout()
        btnMarcar = QPushButton("Marcar como Devuelto")
        btnMarcar.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton)))
        
        #Añadimos los Widget
        layout_botones.addWidget(btnMarcar)

        #Al layout principal le pasamos el layout creado
        layout.addLayout(layout_botones)
        
        return widget