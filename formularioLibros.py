
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QTableView, QHeaderView, QMessageBox, QStyle, QStyleOption
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex 
)

from funcionesAuxiliares import crear_titulo_util, crear_encabezado_util
from biblioteca import TableModel as BibliotecaTableModel

import datos

class Libros(QWidget):
    # Tab 1
    def __init__(self):
        super().__init__()
        self.layout_principal = QVBoxLayout(self)
        
        self.libro_editando_index = None
        
        # Titulo
        self.layout_principal.addWidget(crear_titulo_util("Gestión de libros y Catalógo"))
        
        # Layout contenedor
        self.layout_contenedor = QHBoxLayout()
        
        # Formulario
        self.layout_contenedor.addWidget(self._crear_formulario_libros())
                 
        # Tabla
        self.layout_contenedor.addWidget(self._crear_tabla_libros())
        
        self.layout_principal.addLayout(self.layout_contenedor)
        
    #----------------------------
    # Crear formulario de libros
    #----------------------------
    def _crear_formulario_libros(self):
        widget = QWidget()
        layout = QGridLayout(widget)
        widget.setMaximumWidth(350)
        
        # Base de Datos de controles del formulario
        self.controles_form = {}
        
        campos = [
            ("Titulo:", "titulo", QLineEdit()),
            ("Autor:", "autor", QLineEdit()),
            ("Tematica:", "tematica", QComboBox()),
            ("Formato:", "formato", QComboBox()),
            ("Editorial:", "editorial", QLineEdit()),
            ("Estanteria:", "estanteria", QLineEdit())
        ]
        
        # Configuramos los ComboBox
        # [num del indice del campo] [num de columna] 
        campos[2][2].addItems(["Ciencia Ficción", "Fantasia", "Historia", "Romance", "Infantil"]) 
        campos[3][2].addItems(["Tapa Dura", "Tapa Blanda", "Revista"])
        
        layout.addWidget(crear_encabezado_util("Datos nuevo libro"), 0, 0, 1, 2) # (label, fila, columna, rowspan, colspan)
        
        for i, (nombre, key, control) in enumerate(campos):
            label = QLabel(nombre)
            label.setBuddy(control)
            
            if nombre == "Titulo:": label.setText("&Titulo:") # Alt + T
            if nombre == "Autor:": label.setText("&Autor:")   # Alt + A
            
            layout.addWidget(label, i + 1, 0) # (label, fila, columna)
            layout.addWidget(control, i + 1, 1)
            
            self.controles_form[key] = control
            
        self.btnGuardar = QPushButton("Guardar libro")
        self.btnGuardar.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton)))  
        self.btnLimpiar = QPushButton("Limpiar campos")
        self.btnLimpiar.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton)))
        
        layout.addWidget(self.btnGuardar, len(campos) + 1, 0, 1, 2) # (widget, row, column, rowspan, colspan)
        layout.addWidget(self.btnLimpiar, len(campos) + 2, 0, 1, 2) # (boton, fila, columna, rowspan, colspan)
        
        # Conexion funcionalidad botones
        self.btnGuardar.clicked.connect(self._guardar_libro)
        self.btnLimpiar.clicked.connect(self._limpiar_campos)
        
        layout.setContentsMargins(20, 20, 20, 20) # (left, top, right, bottom)
        
        return widget
    
    #-----------------------
    # Funcionalidad botones
    #-----------------------
    
    # Boton Guardar un libro
    def _guardar_libro(self):
        titulo = self.controles_form["titulo"].text().strip()
        autor = self.controles_form["autor"].text().strip()
        tematica = self.controles_form["tematica"].currentText()
        formato = self.controles_form["formato"].currentText()
        editorial = self.controles_form["editorial"].text().strip()
        estanteria = self.controles_form["estanteria"].text().strip()
        
        #self.libro_editando_index = 0 # TODO - ELIMINAR ESTO
        
        # Validacion simple
        if not titulo or not autor or not editorial or not estanteria:
            QMessageBox.warning(self, "Campos incompletos", "Por favor, complete todos los campos obligatorios.")
            return
        
        try:
            estanteria = int(estanteria)
        except ValueError:
            QMessageBox.critical(self, "Entrada inválida", "El campo 'Estanteria' debe ser un número entero.")
            return
        
        if self.libro_editando_index is not None:
            # Modificar libro existente
            row = self.libro_editando_index
            libro_id = datos.LIBROS[row][0]  # Mantener el mismo ID
            
            datos.LIBROS[row] = [libro_id, titulo, autor, tematica, formato, editorial, estanteria]
            
            
            # En este punto notificamos al modelo que la fila ha cambiado
            colCount = self.modelo_libros.columnCount()
            topLeft = self.modelo_libros.index(row, 0)
            bottomRight = self.modelo_libros.index(row, colCount - 1)
            
            self.modelo_libros.dataChanged.emit(topLeft, bottomRight, [Qt.DisplayRole, Qt.ToolTipRole]) #
            QMessageBox.information(self, "Libro modificado", f"El libro '{titulo}' ha sido modificado correctamente.")
            
        else: 
            new_id = max(d[0] for d in datos.LIBROS) + 1 if datos.LIBROS else 101
            new_libro = [new_id, titulo, autor, tematica, formato, editorial, estanteria]
            
            # Insertar en BD
            datos.LIBROS.append(new_libro)
            
            # Notificar al modelo que se ha insertado una nueva fila
            new_row_index = len(datos.LIBROS) - 1
            self.modelo_libros.beginInsertRows(QModelIndex(), new_row_index, new_row_index)
            self.modelo_libros.endInsertRows()
            
            QMessageBox.information(self, "Libro guardado", f"El libro '{titulo}' ha sido guardado correctamente.")
            
        self._limpiar_campos()
        
        
    
    # Boton Limpiar campos
    def _limpiar_campos(self):
        for control in self.controles_form.values():
            if isinstance(control, QLineEdit):
                control.clear()
            elif isinstance(control, QComboBox):
                control.setCurrentIndex(0)
        
        # Restablecer estado edición 
        self.libro_editando_index = None
        self.btnGuardar.setText("Guardar Libro")
        QMessageBox.information(self, "Limpiar", "Formulario listo para nuevo registro.")
    
    
    # Boton Eliminar libro
    def _eliminar_libro(self):
        row_index = self._get_selected_row_index()

        if row_index != -1:
            libro_id = datos.LIBROS[row_index][0]

            reply = QMessageBox.question(
                self,
                "Confirmar Eliminación",
                f"¿Está seguro de que desea eliminar el libro ID {libro_id}?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                # Llama al método del modelo para eliminar el libro de la BD
                if self.modelo_libros.removeRow(row_index):
                    QMessageBox.information(self, "Eliminado", f"Libro ID {libro_id} eliminado correctamente.")
                else:
                    QMessageBox.critical(self, "Error", "No se pudo eliminar el libro seleccionado.")

    
    # Obtener el índice de la fila seleccionada en la tabla
    def _get_selected_row_index(self):
        
        selected_rows = self.tabla_libros.selectionModel().selectedRows()
        #Muestra una advertencia si no hay ninguna fila
        if not selected_rows:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un libro para editar.")
            return -1
        # selectedRows devuelve una lista de QModelIndex, tomamos el primer elemento y su row
        return selected_rows[0].row()


    #Cargar los datos del libro seleccionado en el formulario para su edición
    def _editar_libro(self):

        row_index = self._get_selected_row_index()

        if row_index != -1:
            libro_datos = datos.LIBROS[row_index]

            # Cargar datos en el formulario
            self.controles_form["titulo"].setText(libro_datos[1])
            self.controles_form["autor"].setText(libro_datos[2])

            tematica_index = self.controles_form["tematica"].findText(libro_datos[3])
            if tematica_index != -1: self.controles_form["tematica"].setCurrentIndex(tematica_index)

            format_index = self.controles_form["formato"].findText(libro_datos[4])
            if format_index != -1: self.controles_form["formato"].setCurrentIndex(format_index)
                
            self.controles_form["editorial"].setText(libro_datos[5])
            self.controles_form["estanteria"].setText(str(libro_datos[6]))

            # Cambiar estado a edición
            self.libro_editando_index = row_index
            self.btnGuardar.setText("Actualizar Libro")
            QMessageBox.information(self, "Edición", f"Editando libro ID {libro_datos[0]}. Realice los cambios y presione 'Actualizar Libro'.")


    #-----------------------
    # Crear tabla de libros
    #-----------------------
    
    # Esta tabla muestra los libros que tenemos en la biblioteca
    def _crear_tabla_libros(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        cabecera = ["ID", "Título", "Autor", "Temática", "Formulario", "Editorial", "Estantería"]
        self.modelo_libros = BibliotecaTableModel(datos.LIBROS, cabecera)
        
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
        self.btnEditar = QPushButton("Editar Seleccionado")
        self.btnEditar.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogListView)))
        self.btnEli = QPushButton("Eliminar Seleccionado")
        self.btnEli.setIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon)))
        
        #Añadimos los Widget
        layout_botones.addWidget(self.btnEditar)
        layout_botones.addWidget(self.btnEli)
        
        # Conexion funcionalidad botones
        self.btnEditar.clicked.connect(self._editar_libro)
        self.btnEli.clicked.connect(self._eliminar_libro)

        #Al layout principal le pasamos el layout creado
        layout.addLayout(layout_botones)
        
        return widget
        
