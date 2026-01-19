import sys
import os
import re
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QTextBrowser, QTreeWidget, QTreeWidgetItem,
    QLineEdit, QPushButton, QSplitter, QLabel, QFrame, QStyle,
    QTreeWidgetItemIterator
)
from PySide6.QtGui import QFont, QIcon, QAction
from PySide6.QtCore import Qt, QUrl


# Sistema de ayuda de aplicación
class VentanaAyuda(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sistema de Ayuda - Biblioteca")
        self.setWindowIcon(QIcon("img/help_icon.jpg"))
        self.resize(900, 600)

        #Ruta para los documentos html
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        self.base_path = os.path.join(ruta_script, "docs")

        #Vefiricacion 
        self.historial_atras = []
        self.historial_adelante = []
        self.pagina_actual = ""
        self.bloquear_historial = False
        self.ultimo_termino_buscado = ""

        #Widget central y layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        #Configurar interfaz
        self.setup_search_bar()
        self.setup_navigation_bar()
        self.splitter = QSplitter(Qt.Horizontal)

        self.setup_index_tree()
        self.setup_content_viewer()

        self.main_layout.addWidget(self.splitter)

        #Carga por defecto
        self.cargar_archivo_html("bienvenida.html")
        
        
    def setup_navigation_bar(self):
        nav_layout = QHBoxLayout()
        
        self.btn_atras = QPushButton("Atrás")
        self.btn_adelante = QPushButton("Adelante")
        
        self.btn_atras.setEnabled(False)
        self.btn_adelante.setEnabled(False)
        
        self.btn_atras.clicked.connect(self.on_button_atras_clicked)
        self.btn_adelante.clicked.connect(self.on_button_adelante_clicked)
        
        nav_layout.addWidget(self.btn_atras)
        nav_layout.addWidget(self.btn_adelante)
        nav_layout.addStretch()
        
        self.main_layout.addLayout(nav_layout)
        
        
    def on_button_atras_clicked(self):
        self.historial_adelante.append(self.pagina_actual)
        archivo = self.historial_atras.pop()
        
        # Bloqueamos registro
        self.bloquear_historial = True
        



    def setup_index_tree(self):
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Indice de ayuda")
        self.tree.setMidLineWidth(250)

        #Estructura del arbol de documentos
        root = QTreeWidgetItem(self.tree, ["Manual de usuario"])

        item_bienvenida = QTreeWidgetItem(root, ["Bienvenida"])
        item_bienvenida.setData(0, Qt.UserRole, "bienvenida.html")

        item_modulos = QTreeWidgetItem(root, ["Módulos del sistema"])
        
        item_modulo_libros = QTreeWidgetItem(item_modulos, ["Gestión de Libros"])
        item_modulo_libros.setData(0, Qt.UserRole, "modulo_libros.html")
        item_modulo_prestamos = QTreeWidgetItem(item_modulos, ["Gestión de Préstamos"])
        item_modulo_prestamos.setData(0, Qt.UserRole, "modulo_prestamos.html")
    
        self.tree.expandAll()
        self.tree.itemClicked.connect(self.on_tree_item_clicked)
        self.splitter.addWidget(self.tree)
        

    def setup_content_viewer(self):
        self.viewer = QTextBrowser()
        # Rutas de busquedad para recursos internos
        self.viewer.setSearchPaths([self.base_path])
        self.viewer.setFrameStyle(QFrame.NoFrame)
        self.splitter.addWidget(self.viewer)
    
    
    def on_tree_item_clicked(self, item, column):
        nombre_archivo = item.data(0, Qt.UserRole)
        if nombre_archivo:
            self.cargar_archivo_html(nombre_archivo)
    

    def setup_search_bar(self):
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar en archivos locales...")
        btn_buscar = QPushButton("Buscar")

        search_layout.addWidget(QLabel("🔍"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(btn_buscar)
        self.main_layout.addLayout(search_layout)
        
        

    def cargar_archivo_html(self, nombre_archivo):
        ruta_completa = os.path.join(self.base_path, nombre_archivo)
        
        if not self.bloquear_historial:
            self.historial_atras.append(self.pagina_actual)
            self.historial_adelante.clear()
            
        self.pagina_actual = nombre_archivo
        ruta_completa = os.path.join(self.base_path, nombre_archivo)
        
        if os.path.exists(ruta_completa):
            self.viewer.setSource(QUrl.fromLocalFile(ruta_completa))
        else:
            self.viewer.setHtml(
                f"<h1 style='color:red;'>Error de Ruta</h1>"
                f"<p>No se pudo encontrar el archivo: {nombre_archivo}</p>"
                f"<p>Verifique que el archivo exista en la ruta correcta.</p>"
            )
    
    
    # Manejo del evento de búsqueda
    def on_buttonBusc_clicked(self):
        #Buscar si lo escrito existe dentro del contenido declos html y mostrar las páginas html que lo contienen
        termino_busqueda = self.search_input.text().lower().strip()
        if not termino_busqueda:
            return
        resultados = []
        for archivo in os.listdir(self.base_path):
            if archivo.endswith(".html"):
                ruta_completa = os.path.join(self.base_path, archivo)
                try:
                    with open(ruta_completa, 'r', encoding='utf-8') as f:
                        contenido = f.read().lower()
                        # Esto evita que el buscador encuentre terminos dentro de <style> o <div>
                        texto_plano = re.sub('<[^<]+?>', ' ', contenido).lower()
                        if termino_busqueda in texto_plano:
                            resultados.append(archivo)  
                except Exception as e:
                    print(f"Error al leer el archivo {archivo}: {e}")     
        # Comprobamos si hay resultados y los mostramos
        self.mostrar_resultados_busqueda(resultados)
            
            
    # Función para mostrar los resultados de la búsqueda    
    def mostrar_resultados_busqueda(self, resultados):
        if resultados:
            html_resultados = "<h2>Resultados de la búsqueda:</h2><ul>"
            for archivo in resultados:
                nombre_mostrar = archivo.replace(".html", "").replace("_", " ").title()
                html_resultados += f'<li><a href="{archivo}">{nombre_mostrar}</a></li>'
            html_resultados += "</ul>"
            self.viewer.setHtml(html_resultados)


# INICIACION
if __name__ == "__main__":
    app = QApplication(sys.argv) #Asegurarnos de que los argumentos de la linea de comandos pasen por Qt
    app.setStyle("Fusion")  #Estilo de la aplicación
    ventana = VentanaAyuda()  
    ventana.show()
    sys.exit(app.exec()) #Inicia el bucle y espera a que la ventana se cierre