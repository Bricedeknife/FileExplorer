import sys
import random
from PyQt5.QtWidgets import ( QGraphicsEllipseItem,
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QGraphicsView, QGraphicsScene, QFileDialog, QLabel, QMenuBar
)
from PyQt5.QtGui import QColor, QBrush, QWheelEvent, QPainter
from PyQt5.QtCore import Qt, QPointF, QTimer
import ntpath
import os
from file_bubble import FileBubble

class BubbleView(QGraphicsView):
    def __init__(self, parent =None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)  # Améliore l'apparence des bulles

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setInteractive(True)

        self.gravity = 0  # Intensité de la gravité
        self.timer = QTimer(self)
        self.timer.setInterval(10)  # Interval de rafraîchissement en millisecondes
        self.timer.timeout.connect(self.update_positions)
        self.timer.start()
        self.viewport().setMouseTracking(True)

    def update_positions(self):
        for item in self.scene().items():
            if isinstance(item, FileBubble):
                pos = item.pos()
                velocity = item.data(Qt.UserRole)
                velocity.setY(velocity.y() + self.gravity)  # Ajoute la gravité à la vitesse verticale
                new_pos = pos + velocity
                item.setPos(new_pos)
                item.setData(Qt.UserRole, velocity)

    def wheelEvent(self, event: QWheelEvent):
        zoom_out_factor = 1 / 1.2
        zoom_in_factor = 1.2
        zoom_delta = event.angleDelta().y()

        if zoom_delta > 0:
            self.scale(zoom_in_factor, zoom_in_factor)
        else:
            self.scale(zoom_out_factor, zoom_out_factor)
