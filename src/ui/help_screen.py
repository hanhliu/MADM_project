import json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel, \
    QPushButton

from src.controller import MainController
from src.core.models.paper_model import Paper
from src.core.models.reviewer_model import Reviewer


class HelpScreen(QWidget):
    def __init__(self, parent=None, controller: MainController = None):
        super().__init__(parent)
        self.load_ui_help()
        self.load_ui()

    def load_ui(self):
        # create layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.top_layout = QVBoxLayout()
        self.top_layout.addLayout(self.layout_help)

        self.main_layout.addLayout(self.top_layout)
        self.setLayout(self.main_layout)

    def load_ui_help(self):
        label_choose_topic = QLabel("Trợ giúp tìm người phản biện đề tài: ")
        self.combobox_topic = QPushButton("Chọn đề tài")
        layout_choose_topic = QHBoxLayout()
        layout_choose_topic.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_choose_topic.addWidget(label_choose_topic)
        layout_choose_topic.addWidget(self.combobox_topic)

        label_topic = QLabel("Tên đề tài: ")
        self.label_name_topic = QLabel("Applications of Artificial Intelligence in Medicine")
        layout_topic_hbox = QHBoxLayout()
        layout_topic_hbox.setSpacing(4)
        layout_topic_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_topic_hbox.addWidget(label_topic)
        layout_topic_hbox.addWidget(self.label_name_topic)

        label_author = QLabel("Tác giả: ")
        self.label_author_name = QLabel("Martin")
        layout_author_hbox = QHBoxLayout()
        layout_author_hbox.setSpacing(4)
        layout_author_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_author_hbox.addWidget(label_author)
        layout_author_hbox.addWidget(self.label_author_name)

        hbox_common = QHBoxLayout()
        hbox_common.setSpacing(80)
        hbox_common.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hbox_common.addLayout(layout_topic_hbox)
        hbox_common.addLayout(layout_author_hbox)

        label_field = QLabel("Lĩnh vực: ")
        self.label_field_name = QLabel("Economic")
        layout_field_hbox = QHBoxLayout()
        layout_field_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_field_hbox.addWidget(label_field)
        layout_field_hbox.addWidget(self.label_field_name)

        label_start_date = QLabel("Ngày diễn ra:")
        self.label_date = QLabel("2025-10-20")
        layout_start_date_hbox = QHBoxLayout()
        layout_start_date_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_start_date_hbox.addWidget(label_start_date)
        layout_start_date_hbox.addWidget(self.label_date)

        self.layout_help = QVBoxLayout()
        self.layout_help.addLayout(layout_choose_topic)
        self.layout_help.addLayout(hbox_common)
        self.layout_help.addLayout(layout_field_hbox)
        self.layout_help.addLayout(layout_start_date_hbox)

    def combo_box_change(self):
        pass
