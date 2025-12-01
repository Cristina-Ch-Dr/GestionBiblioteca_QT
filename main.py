import sys
# Importamos PySide6.QtCore con un alias para una referencia más limpia
import PySide6.QtCore as QtCore 
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget,
    QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QTableView, QHeaderView, QMessageBox,
    QStyle, QStyleOption
)
from PySide6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex 
)
from PySide6.QtGui import QFont, QIcon, QPainter, QColor


# Funciones auxiliares
def crear_titulo_util(texto: str) -> QLabel:
    label = QLabel(texto)
    label.setFont(QFont("Palatino Linotype", 24, QFont.Bold))
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return label

def crear_encabezado_util(texto: str) -> QLabel:
    label = QLabel(texto)
    label.setFont(QFont("Palatino Linotype", 16, QFont.Bold))
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return label


# DATOS
DATA_LIBROS = [
    [101, "Cien años de soledad", "García Márquez", "Ficción", "Libro", "Alfaguara", 1],
    [102, "The Lord of the Rings", "J.R.R. Tolkien", "Fantasía", "Libro", "Minotauro", 3],
    [103, "Guía de Programación Qt", "Varios", "Informática", "Multimedia", "Eudeba", 5],
    [104, "El Principito", "A. de Saint-Exupéry", "Infantil", "Libro", "Salamandra", 1]
]

DATA_PRESTAMOS = [
    [1, "101 - Soledad", "Juan Pérez", "15/11/2025", "29/11/2025", "Vigente"],
    [2, "103 - Guía Qt", "María López", "10/11/2025", "10/12/2025", "Vigente"],
    [3, "102 - Rings", "Carlos Ruiz", "01/11/2025", "15/11/2025", "Devuelto"]
]


# MODELOS DE DATOS DEL FORMULARIO 
    # Sirve para gestionar los datos de la tabla de libros
    #  porque si no no se ve nada ya que hereda de QAbstractTableModel
class BibliotecaTableModel(QAbstractTableModel):
    def __init__(self, data, header):
        super().__init__()
        self._data = data
        self._header = header

    # Devolver el número de FILAS
    def rowCount(self, parent = QModelIndex()):
        return len(self._data)

    # Devolver el número de COLUMNAS
    def columnCount(self, parent = QModelIndex()):
        return len(self._header)
    
    # Devolver los datos para cada CELDA
    def data(self, index, role = Qt.DisplayRole):
        # Comprobar que el índice es válido
            # si no es válido o la fila o columna están fuera de rango devolvemos none (nulo)
        if not index.isValid() or index.row() >= self.rowCount() or index.column() >= self.columnCount():
            return None
        
        # Rol principal: mostrar datos
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        
        # Rol de ToolTip: (información al pasar el ratón)
        if role == Qt.ToolTipRole:
            return f"{self._header[index.column()]}: {self._data[index.row()][index.column()]}"
        
        # Rol de fondo (para colorear filas de préstamos)
        if role == Qt.BackgroundRole:
            status = self._data[index.row()][5]  
            if status == "Vigente":
                # Color amarillo para préstamos vigentes
                return QColor(255, 255, 204)
            elif status == "Devuelto":
                # Color verde claro para préstamos devueltos
                return QColor(204, 255, 204)
        # Para otros roles, devolver None
        return None
        

    # Devuelve el encabezado de las columnas
    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._header[section]
        return None 
    

class FormularioLibros(QWidget):
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
        
        
class FormularioPrestamos(QWidget):
    # Tab 2
    def __init__(self):
        super().__init__()
        
class FormularioPersonal(QWidget):
    # Tab 3
    def __init__(self):
        super().__init__()




class MainWindow(QMainWindow):
    # Clase principal
    def __init__(self):
        super().__init__() # Esto hace que herede todo de QWidget
        self.setWindowTitle("Sistema de Biblioteca")
        self.setWindowIcon(QIcon("libros.png"))
        self.setGeometry(100, 100, 1000, 600) # (x, y, ancho y alto)
        
        self.tabs = QTabWidget() # Crear pestañas
        self.setCentralWidget(self.tabs) # Poner las pestañas en la ventana principal
        # Agregar pestañas
        self._setup_tab()
        # Status Bar
        self.statusBar().showMessage("Va to gucci.")
        
        
    def _setup_tab(self):
        self.tab_libros = FormularioLibros() # Crear la pestaña de libros
        # Usando "&" se utiliza atajo Alt + L
        self.tabs.addTab(self.tab_libros, "&Libros")
        self.tab_prestamos = FormularioPrestamos() # Crear la pestaña de prestamos
        self.tabs.addTab(self.tab_prestamos, "&Préstamos")
        self.tab_personal = FormularioPersonal() # Crear la pestaña de personal
        self.tabs.addTab(self.tab_personal, "Personal + &Recursos")
        #Configuracion de tooltips
        self.tabs.setTabToolTip(0, "ALT + L: Ir a Libros")
        self.tabs.setTabToolTip(1, "ALT + P: Ir a Prestamos")
        self.tabs.setTabToolTip(2, "ALT + R: Ir a Recursos")   



# Iniciación para hacerme la chula
if __name__ == "__main__":
    app = QApplication(sys.argv) # sys.argv -> Asegurarnos de que todas las lineas de comandos pasen por Qt    
    # Configurar un estilo
    app.setStyle("Fusion")
    # Crear la ventana
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec()) # Cuando le puses a la X que se cierre la app
    
    