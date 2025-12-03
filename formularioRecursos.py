
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QTableView, QHeaderView, QMessageBox, QStyle, QStyleOption
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QPainter, QColor

from funcionesAuxiliares import crear_titulo_util, crear_encabezado_util


class Recursos(QWidget):
    # Tab 3
    def __init__(self):
        super().__init__()
        
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setAlignment(Qt.AlignTop)
        # Layout contenedor
        self.layout_contenedor = QHBoxLayout()
        
        self.layout_principal.addWidget(crear_titulo_util("Administración de Personal y Recursos"))
        self.layout_principal.addWidget(self._crear_formulario_bibliotecario())
        self.layout_principal.addWidget(self._crear_formulario_espacios())
        
        self.layout_principal.addLayout(self.layout_contenedor)
        
        
    def _crear_formulario_bibliotecario(self):
        group_widget = QWidget()
        group_widget.setMaximumHeight(150)
        layout = QGridLayout(group_widget)
        
        # Campos del formulario
        campos = [
            ("Nombre:", QLineEdit()),
            ("Sala Asignada:", QComboBox())
        ]
        
        # Configuracion de combobox
        campos[1][1].addItems(["Sala 1", "Sala 2", "Sala 3"])
        
        # Usabilidad: Agrupar campos en Grid
        layout.addWidget(crear_encabezado_util("---Gestión de Bibliotecarios---"), 0, 0, 1, 2)
        
        for i, (nombre, control) in enumerate(campos):
            label = QLabel(nombre)
            label.setBuddy(control)
            
            
            layout.addWidget(label, i + 1, 0) # (label, fila, columna)
            layout.addWidget(control, i + 1, 1)
            
        # Boton de accion al final de la fila de los campos
        btnAgregar = QPushButton("Añadir Bibliotecario")
        btnAgregar.setIcon(QIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton)))
        layout.addWidget(btnAgregar, len(campos) + 1, 0, 2, 2)

        return group_widget
    
    
    
    def _crear_formulario_espacios(self):
        group_widget = QWidget()
        group_widget.setMaximumHeight(150)
        layout = QGridLayout(group_widget)
        
        # Campos del formulario
        campos = [
            ("Sala ID:", QLineEdit()),
            ("Estanterías:", QLineEdit())
        ]
                
        # Usabilidad: Agrupar campos en Grid
        layout.addWidget(crear_encabezado_util("---Gestión de Espacios---"), 0, 0, 1, 2)
        
        for i, (nombre, control) in enumerate(campos):
            label = QLabel(nombre)
            label.setBuddy(control)
            
            
            layout.addWidget(label, i + 1, 0) # (label, fila, columna)
            layout.addWidget(control, i + 1, 1)
            
        # Boton de accion al final de la fila de los campos
        btnAgregar = QPushButton("Guardar Sala")
        btnAgregar.setIcon(QIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton)))
        layout.addWidget(btnAgregar, len(campos) + 1, 0, 2, 2)

        return group_widget