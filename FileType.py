import sys
from random import randint
from PyQt5.QtWidgets import QApplication ,QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QColor


class MovingObject(QGraphicsRectItem):
    def __init__(self, x, y, h,w, app = None, c = "red"):
        super().__init__(0, 0, w, h)
        self.app = app
        self.color = QColor(c)
        self.setPos(x, y)
       #self.setBrush(Qt.blue)
        self.setBrush(self.color)
        self.setAcceptHoverEvents(True)
    # mouse hover event
    def hoverEnterEvent(self, event):
        self.app.instance().setOverrideCursor(Qt.CursorShape.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        self.app.instance().restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        print("clicked")

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))


class FichierJPG(MovingObject):
    def __init__(self,x,y,h,w, app = None, c = "red"):
        super().__init__(x,y,w,h,app, c)

class FichierPdf(MovingObject):
    def __init__(self,x,y,h,w, app = None, c = "blue"):
        super().__init__(x,y,w,h,app, c)


'''     '''

