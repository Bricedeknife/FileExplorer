import sys
import random
from PyQt5.QtWidgets import ( QGraphicsEllipseItem, QGraphicsRectItem, 
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QGraphicsView, QGraphicsScene, QFileDialog, QLabel, QMenuBar,QGraphicsTextItem
)
from PyQt5.QtGui import QColor, QBrush, QWheelEvent, QPainter, QFont, QPen
from PyQt5.QtCore import Qt, QPointF, QTimer, QMarginsF 
import ntpath
import os
from bubble_view import BubbleView
from file_bubble import FileBubble


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.directory_counter = 0 
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

    def get_positions(self):
        base_x = (self.directory_counter % 10) * 2000  # Change 10 and 200 based on your needs
        base_y = (self.directory_counter // 10) * 2000

        positions = []
        for i in range(50):  # Increase the range value if you have more than 50 files in a subfolder
            x = base_x
            y = base_y + i * 20  # Increase y coordinate for each new file
            positions.append((x, y))
        return positions



    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select a file", "", "Text files (*.txt)")
        if file_path:
            with open(file_path, 'r', encoding='macRoman') as file:
                content = file.read()
                nombre = len(content.split('\n'))
                self.bubble_view.scene().clear()  # Clear the scene

                file_name = file_path.split("/")[-1]  # Get the file name without the path
                self.label_selected_file.setText(f"Selected file: {file_name}")

        directory_positions = {}
        directory_items = {}
        for index, line in enumerate(content.split("\n")):
            File_Name, File_type = self.extract_file_info(line)
            bubble = FileBubble(File_Name, File_type, line)

            directory = os.path.dirname(line)
            if directory not in directory_positions:
                directory_positions[directory] = {
                    'positions': self.get_positions(),
                    'current_index': 0
                }
                self.directory_counter += 1

            positions = directory_positions[directory]['positions']
            current_index = directory_positions[directory]['current_index']
            x, y = positions[current_index % len(positions)]
            bubble.setPos(x, y)
            directory_positions[directory]['current_index'] += 1

            self.bubble_view.scene().addItem(bubble)

            # Get or create the rect_item for this directory
            rect_item = directory_items.get(directory)
            if rect_item is None:
                rect_item = QGraphicsRectItem()
                self.bubble_view.scene().addItem(rect_item)
                directory_items[directory] = rect_item

                # Add the directory name above the rectangle
                text_item = QGraphicsTextItem(directory, rect_item)
                text_item.setPos(rect_item.rect().x(), rect_item.rect().y() - text_item.boundingRect().height())

            # Compute the new rectangle
            united_rect = rect_item.rect().united(bubble.sceneBoundingRect())
            margined_rect = united_rect.adjusted(-1, -1, 1, 1)
            rect_item.setRect(margined_rect)
            rect_item.setFlags(rect_item.ItemIsMovable)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
