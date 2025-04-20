from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QComboBox, \
    QHBoxLayout, QPushButton, QDoubleSpinBox, QSpinBox

from src.controller import MainController
from src.core.models.paper_model import Paper
from src.core.models.reviewer_model import Reviewer


class AddDataScreen(QWidget):
    def __init__(self, parent=None, controller: MainController=None, papers=None, reviewers=None):
        super().__init__(parent)
        self.controller = controller
        self.papers = papers
        self.reviewers = reviewers
        self.load_ui_add_user()
        self.load_ui_add_topic()
        self.load_ui()
        self.setup_stylesheet()

    def load_ui(self):
        # create layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.main_layout.addWidget(self.add_topic_widget)
        self.main_layout.addWidget(self.add_user_widget)
        self.setLayout(self.main_layout)

    def load_ui_add_topic(self):
        self.add_topic_layout = QVBoxLayout()
        self.add_topic_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.add_user_layout.setSpacing(10)
        self.add_topic_widget = QWidget()
        self.add_topic_widget.setLayout(self.add_topic_layout)

        label = QLabel("Đề tài:")
        self.input_topic_name = QLineEdit()
        self.input_topic_name.setPlaceholderText("Nhập tên đề tài")
        layout_name_topic = QVBoxLayout()
        layout_name_topic.addWidget(label)
        layout_name_topic.addWidget(self.input_topic_name)

        label_field = QLabel("Lĩnh vực:")
        self.combo_box_field = QLineEdit()
        self.combo_box_field.setPlaceholderText("Nhập các lĩnh vực, cách nhau bằng dấu phẩy")
        layout_field = QVBoxLayout()
        layout_field.addWidget(label_field)
        layout_field.addWidget(self.combo_box_field)

        label_time = QLabel("Thời gian:")
        self.input_time = QLineEdit()
        self.input_time.setPlaceholderText("Nhập thời gian diễn ra")
        self.input_time.setToolTip("Nhập thời gian theo định dạng YYYY-MM-DD (VD: 2025-06-01)")
        self.input_time.setMaxLength(10)  # Giới hạn độ dài tối đa của chuỗi nhập vào
        layout_time = QVBoxLayout()
        layout_time.addWidget(label_time)
        layout_time.addWidget(self.input_time)

        label_authors = QLabel("Tác giả:")
        self.input_authors = QLineEdit()
        self.input_authors.setPlaceholderText("Nhập tên tác giả")
        self.input_authors.setToolTip("Nhập tên tác giả, cách nhau bằng dấu phẩy")
        layout_authors = QVBoxLayout()
        layout_authors.addWidget(label_authors)
        layout_authors.addWidget(self.input_authors)

        label_degree_requirement = QLabel("Học vị yêu cầu:")
        self.combobox_degree_requirement = QComboBox()
        self.combobox_degree_requirement.setPlaceholderText("Chọn học vị yêu cầu")
        self.combobox_degree_requirement.addItems(["Masters", "PhD"])
        layout_degree_requirement = QVBoxLayout()
        layout_degree_requirement.addWidget(label_degree_requirement)
        layout_degree_requirement.addWidget(self.combobox_degree_requirement)

        label_add_topic = QLabel("Thêm đề tài:")

        layout_1 = QHBoxLayout()
        layout_1.addLayout(layout_name_topic)
        layout_1.addLayout(layout_field)
        layout_1.addLayout(layout_time)

        layout_2 = QHBoxLayout()
        layout_2.addLayout(layout_authors)
        layout_2.addLayout(layout_degree_requirement)

        button_add_topic = QPushButton("Thêm đề tài")
        button_add_topic.setFixedWidth(200)
        button_add_topic.clicked.connect(self.add_topic)

        self.add_topic_layout.addWidget(label_add_topic)
        self.add_topic_layout.addLayout(layout_1)
        self.add_topic_layout.addLayout(layout_2)
        self.add_topic_layout.addWidget(button_add_topic)

    def load_ui_add_user(self):
        self.add_user_layout = QVBoxLayout()
        self.add_user_layout.setSpacing(10)

        self.add_user_widget = QWidget()
        self.add_user_widget.setLayout(self.add_user_layout)

        # Tên người dùng
        label_name = QLabel("Họ tên:")
        self.input_reviewer_name = QLineEdit()
        self.input_reviewer_name.setPlaceholderText("Nhập tên reviewer")
        layout_name = QVBoxLayout()
        layout_name.addWidget(label_name)
        layout_name.addWidget(self.input_reviewer_name)

        # Lĩnh vực (có thể nhiều)
        label_field = QLabel("Lĩnh vực:")
        self.input_reviewer_field = QLineEdit()
        self.input_reviewer_field.setPlaceholderText("Nhập các lĩnh vực, cách nhau bằng dấu phẩy")
        layout_field = QVBoxLayout()
        layout_field.addWidget(label_field)
        layout_field.addWidget(self.input_reviewer_field)

        # Học vị
        label_degree = QLabel("Học vị:")
        self.combo_box_reviewer_degree = QComboBox()
        self.combo_box_reviewer_degree.setPlaceholderText("Chọn học vị")
        self.combo_box_reviewer_degree.addItems(["Masters", "PhD"])
        layout_degree = QVBoxLayout()
        layout_degree.addWidget(label_degree)
        layout_degree.addWidget(self.combo_box_reviewer_degree)

        # Chủ đề hội nghị
        label_topic = QLabel("Chủ đề hội nghị:")
        self.input_reviewer_topic = QLineEdit()
        self.input_reviewer_topic.setPlaceholderText("Bài báo trong hội nghị")
        layout_topic = QVBoxLayout()
        layout_topic.addWidget(label_topic)
        layout_topic.addWidget(self.input_reviewer_topic)

        # Đánh giá trung bình
        label_rating = QLabel("Đánh giá trung bình:")
        self.input_reviewer_rating = QDoubleSpinBox()
        self.input_reviewer_rating.setRange(0.0, 5.0)
        self.input_reviewer_rating.setDecimals(1)
        self.input_reviewer_rating.setSingleStep(0.1)
        layout_rating = QVBoxLayout()
        layout_rating.addWidget(label_rating)
        layout_rating.addWidget(self.input_reviewer_rating)

        # Số năm kinh nghiệm
        label_experience = QLabel("Số năm kinh nghiệm:")
        self.input_experience = QSpinBox()
        self.input_experience.setRange(0, 100)
        layout_experience = QVBoxLayout()
        layout_experience.addWidget(label_experience)
        layout_experience.addWidget(self.input_experience)

        # Số bài báo đã xuất bản
        label_published = QLabel("Số bài báo:")
        self.input_published = QSpinBox()
        self.input_published.setRange(0, 1000)
        layout_published = QVBoxLayout()
        layout_published.addWidget(label_published)
        layout_published.addWidget(self.input_published)

        # Thời gian sẵn sàng
        label_availability = QLabel("Thời gian sẵn sàng:")
        self.input_availability = QLineEdit()
        self.input_availability.setPlaceholderText(
            "Nhập thời gian, cách nhau bằng dấu phẩy (VD: 2025-06-01, 2025-06-02)")
        layout_availability = QVBoxLayout()
        layout_availability.addWidget(label_availability)
        layout_availability.addWidget(self.input_availability)

        # Nhãn
        label_add_user = QLabel("Thêm người dùng (reviewer):")

        # Gom layout theo hàng
        layout_1 = QHBoxLayout()
        layout_1.addLayout(layout_name)
        layout_1.addLayout(layout_field)
        layout_1.addLayout(layout_degree)

        layout_2 = QHBoxLayout()
        layout_2.addLayout(layout_topic)
        layout_2.addLayout(layout_rating)
        layout_2.addLayout(layout_experience)

        layout_3 = QHBoxLayout()
        layout_3.addLayout(layout_published)
        layout_3.addLayout(layout_availability)

        # Nút thêm người dùng
        button_add_user = QPushButton("Thêm người dùng")
        button_add_user.setFixedWidth(200)
        button_add_user.clicked.connect(self.add_user)  # cần có hàm add_user

        # Thêm vào layout chính
        self.add_user_layout.addWidget(label_add_user)
        self.add_user_layout.addLayout(layout_1)
        self.add_user_layout.addLayout(layout_2)
        self.add_user_layout.addLayout(layout_3)
        self.add_user_layout.addWidget(button_add_user)

    def add_topic(self):
        topic = self.input_topic_name.text()
        field_str = self.combo_box_field.text()
        field = [f.strip() for f in field_str.split(",") if f.strip()]
        date_str = self.input_time.text()
        authors = [a.strip() for a in self.input_authors.text().split(",") if a.strip()]
        degree_requirement = self.combobox_degree_requirement.currentText()

        if not topic or not field or not date_str or not authors:
            print("Vui lòng nhập đầy đủ thông tin đề tài.")
            return

        try:
            paper_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Định dạng ngày không hợp lệ. Vui lòng dùng YYYY-MM-DD.")
            return
        print("paper_date", paper_date)
        topic_id = self.controller.generate_paper_id()
        paper = Paper(id=topic_id, topic=topic, field=field, date=paper_date,
                      authors=authors, reviewer_degree_requirement=degree_requirement)

        self.controller.add_topic(paper)
        print("Đề tài đã được thêm thành công.")

    def add_user(self):
        name = self.input_reviewer_name.text()
        field = [f.strip() for f in self.input_reviewer_field.text().split(",") if f.strip()]
        degree = self.combo_box_reviewer_degree.currentText()
        topic = self.input_reviewer_topic.text()
        rating = self.input_reviewer_rating.value()
        experience = self.input_experience.value()
        published = self.input_published.value()
        availability = [a.strip() for a in self.input_availability.text().split(",") if a.strip()]

        if not name or not field or not topic or not availability:
            print("Vui lòng nhập đầy đủ thông tin người dùng.")
            return
        print("availability", availability)
        reviewer_id = self.controller.generate_paper_id()  # hoặc generate_reviewer_id()
        reviewer = Reviewer(id=reviewer_id, name=name, field=field, degree=degree,
                            conference_topic=topic, average_rating=rating,
                            years_of_experience=experience, published_papers=published,
                            availability=availability)

        self.controller.add_reviewer(reviewer)
        print("Người dùng đã được thêm thành công.")

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
        self.setStyleSheet(f'''
             QPushButton{{
                background-color: #7E0A0A;
                color: white;
                border-radius: 2px;
                padding: 4px 4px 4px 4px;
            }}
            
             QLineEdit {{
                border: 1px solid #ccc;
                border-radius: 2px;
                padding: 6px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 1px solid #0078d7;
                background-color: #f0f8ff;
            }}
            
            QComboBox {{
                border: 1px solid #ccc;
                border-radius: 2px;
                padding: 5px;
                font-size: 13px;
                background-color: white;
            }}
            QComboBox:hover {{
                border: 1px solid #888;
            }}
            QComboBox:focus {{
                border: 1px solid #3b82f6;
                background-color: #f0f8ff;
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid #ccc;
                selection-background-color: #3b82f6;
                selection-color: white;
            }}
            
            QSpinBox, QDoubleSpinBox {{
                border: 1px solid #ccc;
                border-radius: 2px;
                padding: 4px 8px;
                font-size: 13px;
                background-color: white;
            }}
            QSpinBox:focus, QDoubleSpinBox:focus {{
                border: 1px solid #3b82f6;
                background-color: #f0f8ff;
            }}
            QSpinBox::up-button, QDoubleSpinBox::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
                border-left: 1px solid #ccc;
                border-bottom: 1px solid #ccc;
                background-color: #f2f2f2;
            }}
            QSpinBox::down-button, QDoubleSpinBox::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-left: 1px solid #ccc;
                border-top: 1px solid #ccc;
                background-color: #f2f2f2;
            }}
            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow,
            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
                width: 8px;
                height: 8px;
            }}
            
            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
                image: url("src/assets/chevron_big_up.svg"); 
            }}
            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
                image: url("src/assets/chevron_big_down.svg");
            }}

        ''')