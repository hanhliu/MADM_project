
import sys
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout, QTabWidget

from src.controller import MainController
from src.ui.help_screen import HelpScreen
from src.ui.home_screen import HomeScreen


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_controller = MainController()
        self.load_ui()

    def load_ui(self):
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()

        home_screen = HomeScreen(papers=self.main_controller.papers, reviewers=self.main_controller.reviewers)
        help_screen = HelpScreen(controller=self.main_controller)
        self.tabs = QTabWidget()
        self.tabs.addTab(home_screen, "Thông tin")
        self.tabs.addTab(help_screen, "Trợ giúp")

        self.central_layout.addWidget(self.tabs)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        self.setMinimumSize(920, 700)
        self.center()

    def center(self):
        # Lấy màn hình hiện tại
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Tính toán vị trí trung tâm
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        # Đặt vị trí cửa sổ
        self.move(x, y)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
