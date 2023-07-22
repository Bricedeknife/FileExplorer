import sys
import random
from PyQt5.QtWidgets import ( QGraphicsEllipseItem,
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QGraphicsView, QGraphicsScene, QFileDialog, QLabel, QMenuBar, QToolTip
)
from PyQt5.QtGui import QColor, QBrush, QWheelEvent, QPainter, QCursor
from PyQt5.QtCore import Qt, QPointF, QTimer
import ntpath
import os

class FileBubble(QGraphicsEllipseItem):
    def __init__(self, file_name, file_type, file_path):
        super().__init__()

        self.file_name = file_name
        self.file_type = file_type
        self.file_path = file_path
        self.drag = 0.90  # Facteur de décélération (0.90 pour un ralentissement progressif)
        self.setFlag(self.ItemIsMovable)  # Rend la bulle déplaçable
        self.setFlag(self.ItemSendsGeometryChanges)  # Active les notifications de changement de géométrie
        self.drag = 0.95

        # Ajoutez une constante pour la taille normale
        self.normal_size = 15  # Taille de la bulle
        self.setRect(0, 0, self.normal_size, self.normal_size)
        # Ajoutez une constante pour la taille sur le survol
        self.hover_size = self.normal_size * 3

        # Définis la couleur en fonction du type de fichier
        if file_type == '.pdf':
            self.setBrush(QBrush(Qt.red))
        elif file_type == '.acd':
            self.setBrush(QBrush(Qt.yellow))
        elif file_type == '.docx':
            self.setBrush(QBrush(Qt.white))
        else:
            self.setBrush(QBrush(Qt.gray))  # Autres types de fichiers

        self.setData(Qt.UserRole, QPointF(0, 0))  # Initialise la vitesse à (0, 0)
        self.setToolTip("")
        self.setAcceptHoverEvents(True)


    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        velocity = self.data(Qt.UserRole)
        # Mettre à jour la vitesse uniquement si la bulle est en mouvement
        if velocity.manhattanLength() > 0:
            # Appliquer la décélération
            velocity *= self.drag
            self.setData(Qt.UserRole, velocity)

    def hoverEnterEvent(self, event):
        super().hoverEnterEvent(event)
        QToolTip.showText(QCursor.pos(), f"{self.file_name} - > {self.file_path}")  # Afficher le tooltip
        self.setRect(0,0,self.hover_size,self.hover_size)

    def hoverLeaveEvent(self, event):
        super().hoverLeaveEvent(event)
        self.setRect(0,0,self.normal_size,self.normal_size)
        QToolTip.showText(QCursor.pos(), "")  # Afficher le tooltip

