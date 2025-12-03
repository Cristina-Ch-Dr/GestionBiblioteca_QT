
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QTableView, QHeaderView, QMessageBox, QStyle, QStyleOption
)
from PySide6.QtGui import QIcon

from funcionesAuxiliares import crear_titulo_util, crear_encabezado_util
from biblioteca import TableModel as BibliotecaTableModel

from main import DATA_LIBROS, DATA_PRESTAMOS

class Libros(QWidget):
    # Tab 1
    def __init__(self):
        super().__init__()
        self.layout_principal = QVBoxLayout(self)
        # Titulo
        self.layout_principal.addWidget(crear_titulo_util("Gestión de libros y Catalógo"))
        
        # Layout contenedor
        self.layout_contenedor = QHBoxLayout()
        
        # Formulario
        self.layout_contenedor.addWidget(self._crear_formulario_libros())
        
        # Tabla
        self.layout_contenedor.addWidget(self._crear_tabla_libros())
        
        self.layout_principal.addLayout(self.layout_contenedor)
        
    def _crear_formulario_libros(self):
        widget = QWidget()
        layout = QGridLayout(widget)
        widget.setMaximumWidth(350)
        
        campos = [
            ("Titulo:", QLineEdit()),
            ("Autor:", QLineEdit()),
            ("Editoral:", QLineEdit()),
            ("Tematica:", QComboBox()),
            ("Formato:", QComboBox()),
            ("Estanteria:", QLineEdit())
        ]
        
        # Configuramos los ComboBox
        # [num del indice del campo] [num de columna] 
        campos[3][1].addItems(["Ciencia Ficción", "Fantasia", "Historia", "Romance", "Infantil"]) 
        campos[4][1].addItems(["Tapa Dura", "Tapa Blanda", "Revista"])
        
        layout.addWidget(crear_encabezado_util("Datos nuevo libro"), 0, 0, 1, 2) # (label, fila, columna, rowspan, colspan)
        
        for i, (nombre, control) in enumerate(campos):
            label = QLabel(nombre)
            label.setBuddy(control)
            
            if nombre == "Titulo:": label.setText("&Titulo:") # Alt + T
            if nombre == "Autor:": label.setText("&Autor:")   # Alt + A
            
            layout.addWidget(label, i + 1, 0) # (label, fila, columna)
            layout.addWidget(control, i + 1, 1)
            
        btnGuardar = QPushButton("Guardar libro")
        btnGuardar.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton)))  
        btnLimpiar = QPushButton("Limpiar campos")
        btnLimpiar.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton)))
        
        layout.addWidget(btnGuardar, len(campos) + 1, 0, 1, 2) # (widget, row, columna, rowspan, colspan)
        layout.addWidget(btnLimpiar, len(campos) + 2, 0, 1, 2) # (boton, fila, columna, rowspan, colspan)
        
        layout.setContentsMargins(20, 20, 20, 20) # (left, top, right, bottom)
        
        return widget
    
    def _crear_tabla_libros(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        cabecera = ["ID", "Título", "Autor", "Temática", "Formulario", "Editorial", "Estantería"]
        self.modelo_libros = BibliotecaTableModel(DATA_LIBROS, cabecera)
        
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
        btnEditar = QPushButton("Editar Seleccionado")
        btnEditar.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogListView)))
        btnEli = QPushButton("Eliminar Seleccionado")
        btnEli.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon)))
        
        #Añadimos los Widget
        layout_botones.addWidget(btnEditar)
        layout_botones.addWidget(btnEli)

        #Al layout principal le pasamos el layout creado
        layout.addLayout(layout_botones)
        
        return widget
        
