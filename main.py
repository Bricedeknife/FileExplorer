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
from bubble_view import BubbleView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Explorateur de bulles")
        self.showFullScreen()  

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        # Créer une barre de menus personnalisée
        menu_bar = QMenuBar()
        menu1 = menu_bar.addMenu("Menu 1")
        action = menu1.addAction("Option 1")
        # action.triggered.connect(self.some_method) # décommenter ceci pour connecter l'action à une fonction
        layout.addWidget(menu_bar)

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
