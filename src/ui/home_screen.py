import json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem

from src.core.models.paper_model import Paper
from src.core.models.reviewer_model import Reviewer


class HomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.papers = self.load_papers_from_json()
        self.reviewers = self.load_reviewers_from_json()
        self.load_ui_list()
        self.load_ui()

    def load_ui(self):
        # create layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.main_layout.addLayout(self.top_layout)
        self.setLayout(self.main_layout)

    def load_ui_list(self):
        self.table_topic_widget = QWidget()
        self.table_topic_layout = QVBoxLayout()
        self.table_topic_widget.setLayout(self.table_topic_layout)

        self.table_reviewer_widget = QWidget()
        self.table_reviewer_layout = QVBoxLayout()
        self.table_reviewer_widget.setLayout(self.table_reviewer_layout)

        # create table
        self.table_topic = QTableWidget(self)
        self.table_topic.setRowCount(6)  # Only one paper
        self.table_topic.setColumnCount(5)  # Columns: Topic, Field, Date, Authors
        self.table_topic.setHorizontalHeaderLabels(["No", "Topic", "Field", "Date", "Authors"])
        # Populate table
        self.table_topic.setRowCount(len(self.papers))
        for row, paper in enumerate(self.papers):
            self.table_topic.setItem(row, 0, QTableWidgetItem(str(row)))
            self.table_topic.setItem(row, 1, QTableWidgetItem(paper.topic))
            self.table_topic.setItem(row, 2, QTableWidgetItem(", ".join(paper.field)))
            self.table_topic.setItem(row, 3, QTableWidgetItem(paper.date.strftime("%Y-%m-%d")))
            self.table_topic.setItem(row, 4, QTableWidgetItem(", ".join(paper.authors)))
        self.table_topic_layout.addWidget(self.table_topic)

        self.table_reviewer = QTableWidget(self)
        self.table_reviewer.setRowCount(6)  # Only one paper
        self.table_reviewer.setColumnCount(7)  # Columns: Topic, Field, Date, Authors
        self.table_reviewer.setHorizontalHeaderLabels(["No", "Name", "Field", "Degree", "Availability", "Conference Topic", "Average Rating"])
        # Populate table
        self.table_reviewer.setRowCount(len(self.reviewers))
        for row, reviewer in enumerate(self.reviewers):
            self.table_reviewer.setItem(row, 0, QTableWidgetItem(str(row)))
            self.table_reviewer.setItem(row, 1, QTableWidgetItem(reviewer.name))
            self.table_reviewer.setItem(row, 2, QTableWidgetItem(", ".join(reviewer.field)))
            self.table_reviewer.setItem(row, 3, QTableWidgetItem(reviewer.degree))
            self.table_reviewer.setItem(row, 4, QTableWidgetItem(", ".join(reviewer.availability)))
            self.table_reviewer.setItem(row, 5, QTableWidgetItem(reviewer.conference_topic))
            self.table_reviewer.setItem(row, 6, QTableWidgetItem(str(reviewer.average_rating)))
        self.table_reviewer_layout.addWidget(self.table_reviewer)



        self.top_layout = QVBoxLayout()
        self.top_layout.addWidget(self.table_topic_widget)
        self.top_layout.addWidget(self.table_reviewer_widget)

    def load_papers_from_json(self):
        with open("src/core/json/papers.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # Convert JSON data to Paper objects
        papers = [Paper.from_dict(paper) for paper in data["conferences"]]
        return papers

    def load_reviewers_from_json(self):
        with open("src/core/json/reviewers.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # Convert JSON data to Paper objects
        reviewers = [Reviewer.from_dict(paper) for paper in data["researchers"]]
        return reviewers
    
    def setup_table_width(self, width):
        self.table_topic.setColumnWidth(0, 0.025 * width)  # No
        self.table_topic.setColumnWidth(1, 0.3 * width)  # Topic
        self.table_topic.setColumnWidth(2, 0.2 * width)  # Field
        self.table_topic.setColumnWidth(3, 0.1 * width)  # Date
        self.table_topic.setColumnWidth(4, 0.3 * width)  # Author
    
    def resizeEvent(self, event):
        print(f"HanhLT: self.width = {self.width()}")
        self.setup_table_width(self.width())