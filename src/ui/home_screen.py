
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel

from src.controller import MainController


class HomeScreen(QWidget):
    def __init__(self, parent=None, papers=None, reviewers=None, controller:MainController=None):
        super().__init__(parent)
        self.main_controller = controller
        self.main_controller.signal_change_data.connect(self.refresh_data_and_ui)
        self.papers = papers
        self.reviewers = reviewers
        self.load_ui_list()
        self.load_ui()
        self.setup_stylesheet()

    def load_ui(self):
        # create layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.main_layout.addLayout(self.top_layout)
        self.setLayout(self.main_layout)

    def load_ui_list(self):
        self.table_topic_layout = QVBoxLayout()
        self.table_topic_layout.setSpacing(2)
        self.table_topic_widget = QWidget()
        self.table_topic_widget.setLayout(self.table_topic_layout)

        self.table_reviewer_layout = QVBoxLayout()
        self.table_reviewer_layout.setSpacing(2)
        self.table_reviewer_widget = QWidget()
        self.table_reviewer_widget.setLayout(self.table_reviewer_layout)

        # create table
        self.label_topic_list = QLabel("Danh sách đề tài")
        self.table_topic = QTableWidget(self)

        self.table_topic.setColumnCount(4)  # Columns: Topic, Field, Date, Authors
        self.table_topic.setHorizontalHeaderLabels(["Đề tài", "Lĩnh vực", "Ngày diễn ra", "Tác giả"])
        # Populate table
        self.table_topic.setRowCount(len(self.papers))
        for row, paper in enumerate(self.papers):
            print(f"{paper.topic} - {paper.field} - {paper.date} - {paper.authors}")
            self.table_topic.setItem(row, 0, QTableWidgetItem(paper.topic))
            self.table_topic.setItem(row, 1, QTableWidgetItem(", ".join(paper.field)))
            self.table_topic.setItem(row, 2, QTableWidgetItem(paper.date))
            self.table_topic.setItem(row, 3, QTableWidgetItem(", ".join(paper.authors)))
        self.table_topic.setWordWrap(True)
        self.table_topic.resizeRowsToContents()
        self.table_topic_layout.addWidget(self.label_topic_list)
        self.table_topic_layout.addWidget(self.table_topic)

        self.label_reviewer = QLabel("Danh sách người phản biện")
        self.table_reviewer = QTableWidget(self)
        self.table_reviewer.setRowCount(6)  # Only one paper
        self.table_reviewer.setColumnCount(6)  # Columns: Topic, Field, Date, Authors
        self.table_reviewer.setHorizontalHeaderLabels(["Tên", "Lĩnh vực nghiên cứu", "Học vị", "Ngày sẵn sàng", "Đề tài", "Rate"])
        # Populate table
        self.table_reviewer.setRowCount(len(self.reviewers))
        for row, reviewer in enumerate(self.reviewers):
            self.table_reviewer.setItem(row, 0, QTableWidgetItem(reviewer.name))
            self.table_reviewer.setItem(row, 1, QTableWidgetItem(", ".join(reviewer.field)))
            self.table_reviewer.setItem(row, 2, QTableWidgetItem(reviewer.degree))
            self.table_reviewer.setItem(row, 3, QTableWidgetItem(", ".join(reviewer.availability)))
            self.table_reviewer.setItem(row, 4, QTableWidgetItem(reviewer.conference_topic))
            self.table_reviewer.setItem(row, 5, QTableWidgetItem(str(reviewer.average_rating)))
        self.table_reviewer.setWordWrap(True)
        self.table_reviewer.resizeRowsToContents()
        self.table_reviewer_layout.addWidget(self.label_reviewer)
        self.table_reviewer_layout.addWidget(self.table_reviewer)

        self.top_layout = QVBoxLayout()
        self.top_layout.addWidget(self.table_topic_widget)
        self.top_layout.addWidget(self.table_reviewer_widget)

    def refresh_data_and_ui(self, data):
        self.papers, self.reviewers = data

        # 2. Cập nhật lại bảng đề tài
        self.table_topic.setRowCount(len(self.papers))
        for row, paper in enumerate(self.papers):
            print(f"{paper.topic} - {paper.field} - {paper.date} - {paper.authors}")
            self.table_topic.setItem(row, 0, QTableWidgetItem(paper.topic))
            self.table_topic.setItem(row, 1, QTableWidgetItem(", ".join(paper.field)))
            self.table_topic.setItem(row, 2, QTableWidgetItem(paper.date))
            self.table_topic.setItem(row, 3, QTableWidgetItem(", ".join(paper.authors)))
        self.table_topic.resizeRowsToContents()

        # 3. Cập nhật lại bảng reviewer
        self.table_reviewer.setRowCount(len(self.reviewers))
        for row, reviewer in enumerate(self.reviewers):
            print(f"{reviewer.name} - {reviewer.field} - {reviewer.degree} - {reviewer.availability} - {reviewer.conference_topic} - {reviewer.average_rating}")
            self.table_reviewer.setItem(row, 0, QTableWidgetItem(reviewer.name))
            self.table_reviewer.setItem(row, 1, QTableWidgetItem(", ".join(reviewer.field)))
            self.table_reviewer.setItem(row, 2, QTableWidgetItem(reviewer.degree))
            self.table_reviewer.setItem(row, 3, QTableWidgetItem(", ".join(reviewer.availability)))
            self.table_reviewer.setItem(row, 4, QTableWidgetItem(reviewer.conference_topic))
            self.table_reviewer.setItem(row, 5, QTableWidgetItem(str(reviewer.average_rating)))
        self.table_reviewer.resizeRowsToContents()

    def setup_table_width(self, width):
        self.table_topic.setColumnWidth(0, 0.3 * width)  # Topic
        self.table_topic.setColumnWidth(1, 0.2 * width)  # Field
        self.table_topic.setColumnWidth(2, 0.1 * width)  # Date
        self.table_topic.setColumnWidth(3, 0.28 * width)  # Author

        self.table_reviewer.setColumnWidth(0, 0.1 * width)  # Name
        self.table_reviewer.setColumnWidth(1, 0.15 * width)  # Field
        self.table_reviewer.setColumnWidth(2, 0.1 * width)  # Degree
        self.table_reviewer.setColumnWidth(3, 0.2 * width)  # Availability
        self.table_reviewer.setColumnWidth(4, 0.25 * width)  # Conference topic
        self.table_reviewer.setColumnWidth(5, 0.07 * width)  # Average Rating

    def setup_stylesheet(self):
        self.setStyleSheet("""
            QTableWidget {
                gridline-color: #dcdcdc;
                background-color: #ffffff;
                border: 1px solid #cfcfcf;
                font-size: 14px;
                selection-background-color: #cce7ff;
                selection-color: black;
                alternate-background-color: #f6f6f6;
            }

            QHeaderView::section {
                background-color: #f0f0f0;
                color: #333;
                padding: 4px;
                border: 1px solid #dcdcdc;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 4px;
            }

            QTableCornerButton::section {
                background-color: #f0f0f0;
                border: 1px solid #dcdcdc;
            }
        """)

    def resizeEvent(self, event):
        self.setup_table_width(self.width())
