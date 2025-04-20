
import sys
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout, QTabWidget

from src.controller import MainController
from src.ui.add_data_screen import AddDataScreen
from src.ui.help_screen import HelpScreen
from src.ui.home_screen import HomeScreen


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.screen = QApplication.primaryScreen()
        self.screen_geometry = self.screen.availableGeometry()
        self.main_controller = MainController()
        self.load_ui()
        self.setup_stylesheet()

    def load_ui(self):
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()

        home_screen = HomeScreen(controller=self.main_controller, papers=self.main_controller.papers, reviewers=self.main_controller.reviewers)
        help_screen = HelpScreen(controller=self.main_controller)
        add_data_screen = AddDataScreen(controller=self.main_controller)  # Placeholder for AddDataScreen
        self.tabs = QTabWidget()
        self.tabs.addTab(home_screen, "Thông tin")
        self.tabs.addTab(help_screen, "Trợ giúp")
        self.tabs.addTab(add_data_screen, "Thêm dữ liệu")

        self.central_layout.addWidget(self.tabs)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

    def setup_stylesheet(self):
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ccc;
                background: #f9f9f9;
                top: -1px;
            }
        
            QTabBar::tab {
                background: #e0e0e0;
                border: 1px solid #ccc;
                border-bottom-color: #f9f9f9;
                padding: 8px 20px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
        
            QTabBar::tab:selected {
                background: #7E0A0A;
                color: #ffffff;
                border-color: #ccc;
                border-bottom-color: #ffffff;
            }
        """)


    def resizeEvent(self, event):
        # Tính toán vị trí trung tâm
        width = int(self.screen_geometry.width()*0.7)
        height = int(self.screen_geometry.height()*0.8)
        self.setFixedSize(width, height)
        self.center()

    def center(self):
        # Tính toán vị trí trung tâm
        x = (self.screen_geometry.width() - self.width()) // 2
        y = (self.screen_geometry.height() - self.height()) // 2

        # Đặt vị trí cửa sổ
        self.move(x, y)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
