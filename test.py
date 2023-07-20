import sys
from Connexion import *
from FileType import MovingObject, FichierJPG, FichierPdf, Fichier
from random import randint
from PyQt5.QtWidgets import QApplication ,QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QColor
from data import getFiles

class GraphicView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)       
        self.setSceneRect(0, 0, 70000,70000)
        factor = 50
        a = getFiles("data.txt")
        print(type(a))
        count = 0 
        for i in a:
            if i != None:
                #self.obj = MovingObject(*self._4RandomPoint() ,app, "yellow")

                #self.pdf = FichierPdf(*self._4RandomPoint(),app)
                #self.photo = FichierJPG(*self._4RandomPoint(),app)
                #self.c1 = ConnexionLink(self.pdf,self.obj)
                self.c2 = Fichier(self.scene,*self._4RandomPoint(),i)

                # self.moveObject2 = MovingObject(100, 100, 100)
                self.scene.addWidget(self.c2)
                #self.scene.addItem(self.obj)
                #self.scene.addItem(self.c1)
                #self.scene.addItem(self.pdf)
                #self.scene.addItem(self.photo)
                # self.scene.addItem(self.moveObject2)
                count += 1

        #self.scene.addText("Test", )
        print(count)
    def _4RandomPoint(self):
            x = randint(0,20000)
            y = randint(0,20000)
            h = randint(20,50)
            w = h
            return x,y,h,w




app = QApplication(sys.argv)

view = GraphicView()
view.show()
sys.exit(app.exec_())