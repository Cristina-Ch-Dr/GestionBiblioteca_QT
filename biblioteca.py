
from PySide6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex 
)
from PySide6.QtGui import QFont, QIcon, QPainter, QColor


# MODELOS DE DATOS DEL FORMULARIO 
    # Sirve para gestionar los datos de la tabla de libros
    #  porque si no no se ve nada ya que hereda de QAbstractTableModel
class TableModel(QAbstractTableModel):
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
                return QColor("#F59527")
            elif status == "Devuelto":
                # Color verde oscuro para préstamos devueltos
                return QColor("#2b6b61")
        # Para otros roles, devolver None
        return None
        

    # Devuelve el encabezado de las columnas
    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._header[section]
        return None 
    
    
    def removeRow(self, rowIndex):
        # Inicia el proceso de eliminacion para asegurar que la vista (QTableView) se actualiza correctamente
        if 0 <= rowIndex < len(self._data):
            self.beginRemoveRows(QModelIndex(), rowIndex, rowIndex)
            # Elimina la fila de los datos
            del self._data[rowIndex]
            # Finaliza el proceso de eliminacion
            self.endRemoveRows()
            return True
        return False
    
