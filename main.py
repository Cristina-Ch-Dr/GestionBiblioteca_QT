import sys

# Importamos un módulo externo (debe existir un archivo "ayuda.py" con la clase ventanaAyuda)
try:
    from sistema_ayuda import VentanaAyuda
except ImportError:
    # Fallback preventivo si el archivo no existe durante la edición
    from PySide6.QtWidgets import QWidget
    class VentanaAyuda(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Error: archivo sistema_ayuda.py no existe.")
            

# Importamos PySide6.QtCore con un alias para una referencia más limpia
import PySide6.QtCore as QtCore 
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QTableView, QHeaderView, QMessageBox, QStyle, QStyleOption, QToolBar
)
from PySide6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex 
)
from PySide6.QtGui import QFont, QIcon, QPainter, QColor, QAction

import formularioLibros, formularioPrestamos, formularioRecursos


#------------
# MainWindow
#------------
class MainWindow(QMainWindow):
    # Clase principal
    def __init__(self):
        super().__init__() # Esto hace que herede todo de QWidget
        self.setWindowTitle("Sistema de Biblioteca")
        self.setWindowIcon(QIcon("libros.png"))
        self.setGeometry(100, 100, 1100, 700) # (x, y, ancho y alto)
        
        self.ventana_ayuda = VentanaAyuda(self) # Crear la ventana de ayuda
        self._setup_toolbar() # Configurar la barra de herramientas
        
        self.tabs = QTabWidget() # Crear pestañas
        self.setCentralWidget(self.tabs) # Poner las pestañas en la ventana principal
        # Agregar pestañas
        self._setup_tab()
        # Status Bar
        self.statusBar().showMessage("Va to gucci.")
        
        
    #Función barra de herramientas
    def _setup_toolbar(self):
        toolbar = QToolBar("Barra de herramientas")
        self.addToolBar(toolbar)

        self.action_ayuda = QAction(self.style().standardIcon(QStyle.SP_MessageBoxQuestion), "Ayuda", self)
        self.action_ayuda.triggered.connect(self._mostrar_ayuda)
        
        toolbar.addAction(self.action_ayuda)

    def _mostrar_ayuda(self):
        if self.ventana_ayuda.isHidden():
            self.ventana_ayuda.show()
        else:
            self.ventana_ayuda.activateWindow()
            self.ventana_ayuda.raise_()

    def paintEvent(self, event):
        pass    
        
        
    def _setup_tab(self):
        self.tab_libros = formularioLibros.Libros() # Crear la pestaña de libros
        # Usando "&" se utiliza atajo Alt + L
        self.tabs.addTab(self.tab_libros, "📚 &Libros")
        self.tab_prestamos = formularioPrestamos.Prestamos() # Crear la pestaña de prestamos
        self.tabs.addTab(self.tab_prestamos, "📤 &Préstamos")
        self.tab_personal = formularioRecursos.Recursos() # Crear la pestaña de personal
        self.tabs.addTab(self.tab_personal, "👥 Personal + &Recursos")
        #Configuracion de tooltips
        self.tabs.setTabToolTip(0, "ALT + L: Ir a Libros")
        self.tabs.setTabToolTip(1, "ALT + P: Ir a Prestamos")
        self.tabs.setTabToolTip(2, "ALT + R: Ir a Recursos")   



# Iniciación 
if __name__ == "__main__":
    app = QApplication(sys.argv) # sys.argv -> Asegurarnos de que todas las lineas de comandos pasen por Qt    
    # Configurar un estilo
    app.setStyle("Fusion")
    # Crear la ventana
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec()) # Cuando le puses a la X que se cierre la app
    
    