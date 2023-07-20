import sys

from random import randint
from PyQt5.QtWidgets import QApplication ,QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsLineItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QColor, QPen


class ConnexionLink(QGraphicsLineItem):
    def __init__(self, r1:QGraphicsRectItem ,r2:QGraphicsRectItem):
        rect1_center = r1.sceneBoundingRect().center()
        rect2_center = r2.sceneBoundingRect().center()
        super().__init__(rect1_center.x(), rect1_center.y(), rect2_center.x(), rect2_center.y())

# Get the center point of the rectangles
        

# Create a line between the two rectangles
        line = QGraphicsLineItem(rect1_center.x(), rect1_center.y(), rect2_center.x(), rect2_center.y())
        
        #pen = QPen(QColor(0,0,255))
        #pen.setWidth(13)
        #line.setPen(pen)

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
