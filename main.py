import os
import sys
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout

from src.ui.home_screen import HomeScreen


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.load_ui()

    def load_ui(self):
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()

        home_screen = HomeScreen()
        self.central_layout.addWidget(home_screen)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
