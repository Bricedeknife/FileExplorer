import sys
from Connexion import *
from FileType import MovingObject, FichierJPG, FichierPdf
from random import randint
from PyQt5.QtWidgets import QApplication ,QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QColor


class GraphicView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)       
        self.setSceneRect(0, 0, 1200, 1000)
        factor = 50
        for i in range(0,1000):
            

            self.obj = MovingObject(*self._4RandomPoint() ,app, "yellow")

            self.pdf = FichierPdf(*self._4RandomPoint(),app)
            self.photo = FichierJPG(*self._4RandomPoint(),app)
            self.c1 = ConnexionLink(self.pdf,self.obj)

            # self.moveObject2 = MovingObject(100, 100, 100)
            self.scene.addItem(self.obj)
            self.scene.addItem(self.c1)
            self.scene.addItem(self.pdf)
            self.scene.addItem(self.photo)
            # self.scene.addItem(self.moveObject2)

        self.scene.addText("Test", )
    def _4RandomPoint(self):
            x = randint(0,5000)
            y = randint(0,5000)
            h = randint(20,50)
            w = h
            return x,y,h,w




app = QApplication(sys.argv)

view = GraphicView()
view.show()
sys.exit(app.exec_())