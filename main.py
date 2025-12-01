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
    label.setFont(QFont("Serif", 22, QFont.Bold))
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return label

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
        self.layout_contenedor.addWidget(self.crear_tabla_libros())
        self.layout_principal.addLayout(self.layout_contenedor)
        
    def crear_tabla_libros(self):
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
        
        layout.addWidget(QLabel("Datos nuevo libro"), 0, 0, 1, 2) # (label, fila, columna, rowspan, colspan)
        
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
        self.setGeometry(100, 100, 800, 500) # (x, y, ancho y alto)
        
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
    
    