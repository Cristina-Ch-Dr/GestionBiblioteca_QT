from PySide6.QtWidgets import QLabel

from PySide6.QtGui import QFont, QIcon, QPainter, QColor
from PySide6.QtCore import Qt


# Funcion para crear un título estilizado
def crear_titulo_util(texto: str) -> QLabel:
    label = QLabel(texto)
    label.setFont(QFont("Palatino Linotype", 24, QFont.Bold))
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return label

# Funcion para crear un encabezado estilizado
def crear_encabezado_util(texto: str) -> QLabel:
    label = QLabel(texto)
    label.setFont(QFont("Palatino Linotype", 16, QFont.Bold))
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return label
