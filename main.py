import sys
import random
from PyQt5.QtWidgets import ( QGraphicsEllipseItem,
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QGraphicsView, QGraphicsScene, QFileDialog, QLabel, QMenu
)
from PyQt5.QtGui import QColor, QBrush, QWheelEvent, QPainter
from PyQt5.QtCore import Qt, QPointF, QTimer
import ntpath
import os

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

class FileBubble(QGraphicsEllipseItem):
    def __init__(self, file_name, file_type, file_path):
        super().__init__()

        self.file_name = file_name
        self.file_type = file_type
        self.file_path = file_path
        self.drag = 0.90  # Facteur de décélération (0.90 pour un ralentissement progressif)
        self.setRect(0, 0, 15, 15)  # Taille de la bulle
        self.setFlag(self.ItemIsMovable)  # Rend la bulle déplaçable
        self.setFlag(self.ItemSendsGeometryChanges)  # Active les notifications de changement de géométrie
        self.drag = 0.95

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
        self.setToolTip(f"{self.file_name} - > {self.file_path}")

    def hoverLeaveEvent(self, event):
        super().hoverLeaveEvent(event)
        self.setToolTip("")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Explorateur de bulles")
        self.showMaximized()  # Affiche l'application en plein écran

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Ajouter une barre de menus
        menu_bar = self.menuBar()
        menu1 = QMenu("Menu 1", self)
        menu2 = QMenu("Menu 2", self)
        menu3 = QMenu("Menu 3", self)
        menu4 = QMenu("Menu 4", self)
        menu_bar.addMenu(menu1)
        menu_bar.addMenu(menu2)
        menu_bar.addMenu(menu3)
        menu_bar.addMenu(menu4)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        action = menu1.addAction("Option 1")
        action.triggered.connect(self.some_method)

        
        # Volet des boutons d'options
        options_widget = QWidget(self)
        options_layout = QHBoxLayout(options_widget)
        label_selected_file = QLabel("Fichier sélectionné : ")
        label_Nombre = QLabel("Nombre de fichier : ")
        options_layout.addWidget(label_selected_file)
        options_layout.addWidget(label_Nombre)
        button_option1 = QPushButton("Option 1")
        button_option1.clicked.connect(self.open_file_dialog)
        options_layout.addWidget(button_option1)
        options_layout.addWidget(QPushButton("Option 2"))
        options_layout.addWidget(QPushButton("Option 3"))
        layout.addWidget(options_widget)

        # Espace d'affichage et de navigation des bulles
        bubble_view = BubbleView(self)
        layout.addWidget(bubble_view)

        self.label_selected_file = label_selected_file
        self.label_Nombre = label_Nombre
        self.bubble_view = bubble_view

    def some_method(self):
        print('menu2')
            
    def extract_file_info(self, file_path):
        base_name = ntpath.basename(file_path)
        file_name, file_ext = os.path.splitext(base_name)
        return file_name, file_ext

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Sélectionner un fichier", "", "Fichiers texte (*.txt)")
        if file_path:
            # Traite le fichier sélectionné, par exemple, affiche son contenu
            with open(file_path, 'r', encoding='macRoman') as file:
                content = file.read()
                nombre = len(content.split('\n'))
                self.bubble_view.scene().clear()  # Efface la scène

                # Affiche le nom du fichier sélectionné
                file_name = file_path.split("/")[-1]  # Récupère le nom du fichier sans le chemin
                self.label_selected_file.setText(f"Fichier sélectionné : {file_name}")

                # Parcours chaque ligne et détecte les autres fichiers mentionnés
                for index, line in enumerate(content.split("\n")):
                    File_Name, File_type = self.extract_file_info(line)
                    bubble = FileBubble(File_Name, File_type,line)
                    bubble.setPos(random.randint(0, self.width() - 50), random.randint(0, self.height() - 50))
                    self.bubble_view.scene().addItem(bubble)
                self.label_Nombre.setText(f"Nombre : {nombre}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
