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

import formularioLibros, formularioPrestamos



# DATOS
DATA_LIBROS = [
    [101, "Cien años de soledad", "García Márquez", "Ficción", "Libro", "Alfaguara", 1],
    [102, "The Lord of the Rings", "J.R.R. Tolkien", "Fantasía", "Libro", "Minotauro", 3],
    [103, "Guía de Programación Qt", "Varios", "Informática", "Multimedia", "Eudeba", 5],
    [104, "El Principito", "A. de Saint-Exupéry", "Infantil", "Libro", "Salamandra", 1],
    [105, "1984", "George Orwell", "Ciencia Ficción", "Libro", "Debolsillo", 2],
    [106, "Historia de la humanidad", "Varios", "Historia", "Multimedia", "National Geographic", 4]
]

DATA_PRESTAMOS = [
    [1, "101 - Soledad", "Juan Pérez", "15/11/2025", "29/11/2025", "Vigente"],
    [2, "103 - Guía Qt", "María López", "10/11/2025", "10/12/2025", "Vigente"],
    [3, "102 - Rings", "Carlos Ruiz", "01/11/2025", "15/11/2025", "Devuelto"]
]



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
        self.tab_libros = formularioLibros.Libros() # Crear la pestaña de libros
        # Usando "&" se utiliza atajo Alt + L
        self.tabs.addTab(self.tab_libros, "&Libros")
        self.tab_prestamos = formularioPrestamos.Prestamos() # Crear la pestaña de prestamos
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
    
    