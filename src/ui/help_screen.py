import json
from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QPushButton, QMenu, QTableWidget, QTableWidgetItem
from src.controller import MainController
from PySide6.QtGui import QAction, QFont

from src.core.models.paper_model import Paper


class HelpScreen(QWidget):
    def __init__(self, parent=None, controller: MainController = None):
        super().__init__(parent)
        self.controller = controller
        self.ui_weights()
        self.ui_criteria()
        self.create_decision_table()
        self.ui_decision_table_with_weight()
        self.create_menu()
        self.load_ui_help()
        self.load_ui()

    def ui_criteria(self):
        """Tiêu chí đánh giá:
                    1. Trùng lĩnh vực nghiên cứu - w: 0.3 - Jaccard: số lĩnh vực khớp
                    2. Bằng cấp phù hợp - w: 0.1 - =1 nếu đạt
                    3. Điểm đánh giá cao - w: 0.2 - dùng trực tiếp
                    4. Đã xuất bản nhiều bài báo - w: 0.1 - dùng trực tiếp
                    5. Có nhiều năm nghiên cứu - w: 0.1 - dùng trực tiếp

                    6. Sẵn sàng thời gian - ràng buộc
                    7. Không trùng tác giả -  ràng buộc"""
        self.layout_criteria = QHBoxLayout()
        font = QFont()
        font.setPointSize(10)
        layout_1 = QVBoxLayout()
        layout_2 = QVBoxLayout()
        label_tc = QLabel("TIÊU CHÍ ĐÁNH GIÁ")
        label_1 = QLabel("C1. Trùng lĩnh vực nghiên cứu - w: 0.3 - Jaccard: số lĩnh vực khớp")
        label_2 = QLabel("C2. Bằng cấp phù hợp - w: 0.1 - =1 nếu đạt")
        label_3 = QLabel("C3. Điểm đánh giá cao - w: 0.2 - dùng trực tiếp")
        label_4 = QLabel("C4. Đã xuất bản nhiều bài báo - w: 0.1 - dùng trực tiếp")
        label_5 = QLabel("C5. Có nhiều năm nghiên cứu - w: 0.1 - dùng trực tiếp")
        label_6 = QLabel("R6. Sẵn sàng thời gian - ràng buộc")
        label_7 = QLabel("R7. Không trùng tác giả -  ràng buộc")
        label_1.setFont(font)
        label_2.setFont(font)
        label_3.setFont(font)
        label_4.setFont(font)
        label_5.setFont(font)
        label_6.setFont(font)
        label_7.setFont(font)
        layout_1.addWidget(label_tc)
        layout_1.addWidget(label_1)
        layout_1.addWidget(label_2)
        layout_1.addWidget(label_3)
        layout_2.addWidget(label_4)
        layout_2.addWidget(label_5)
        layout_2.addWidget(label_6)
        layout_2.addWidget(label_7)
        self.layout_criteria.addLayout(layout_1)
        self.layout_criteria.addLayout(layout_2)

    def ui_weights(self):
        label = QLabel("Bộ trọng số")
        self.table_weights = QTableWidget()
        self.table_weights.setRowCount(1)
        self.table_weights.setColumnCount(6)  # Columns: "W1", "W2", "W3", "W4", "W5"
        self.table_weights.setHorizontalHeaderLabels(["", "W1", "W2", "W3", "W4", "W5"])
        # Đặt dữ liệu vào hàng đầu tiên
        self.table_weights.setItem(0, 0, QTableWidgetItem("Trọng số"))
        for col, weight in enumerate(self.controller.weights, start=1):  # Bắt đầu từ cột 1
            self.table_weights.setItem(0, col, QTableWidgetItem(str(weight)))
        push_button = QPushButton("Sửa bộ trọng số")

        layout_temp = QHBoxLayout()
        layout_temp.addWidget(self.table_weights, 9)
        layout_temp.addWidget(push_button, 1)

        self.layout_weight = QVBoxLayout()
        self.layout_weight.setSpacing(2)
        self.layout_weight.addWidget(label)
        self.layout_weight.addLayout(layout_temp)

    def load_ui(self):
        # create layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.top_layout = QVBoxLayout()
        self.top_layout.addLayout(self.layout_help)
        table_layout = QHBoxLayout()
        table_layout.addLayout(self.layout_table_decision)
        table_layout.addLayout(self.layout_table_decision_with_weight)
        self.top_layout.addLayout(table_layout)

        self.main_layout.addLayout(self.top_layout, 10)
        self.main_layout.addLayout(self.layout_weight, 1)
        self.main_layout.addLayout(self.layout_criteria, 1)
        self.setLayout(self.main_layout)

    def load_ui_help(self):
        label_choose_topic = QLabel("Trợ giúp tìm người phản biện đề tài: ")
        self.combobox_topic = QPushButton("Chọn đề tài")
        self.combobox_topic.setMenu(self.menu)
        layout_choose_topic = QHBoxLayout()
        layout_choose_topic.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_choose_topic.addWidget(label_choose_topic)
        layout_choose_topic.addWidget(self.combobox_topic)

        label_topic = QLabel("Tên đề tài: ")
        self.label_name_topic = QLabel("-")
        layout_topic_hbox = QHBoxLayout()
        layout_topic_hbox.setSpacing(4)
        layout_topic_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_topic_hbox.addWidget(label_topic)
        layout_topic_hbox.addWidget(self.label_name_topic)

        label_author = QLabel("Tác giả: ")
        self.label_author_name = QLabel("-")
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
        self.label_field_name = QLabel("-")
        layout_field_hbox = QHBoxLayout()
        layout_field_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_field_hbox.addWidget(label_field)
        layout_field_hbox.addWidget(self.label_field_name)

        label_start_date = QLabel("Ngày diễn ra:")
        self.label_date = QLabel("-")
        layout_start_date_hbox = QHBoxLayout()
        layout_start_date_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_start_date_hbox.addWidget(label_start_date)
        layout_start_date_hbox.addWidget(self.label_date)

        self.layout_help = QVBoxLayout()
        self.layout_help.addLayout(layout_choose_topic)
        self.layout_help.addLayout(hbox_common)
        self.layout_help.addLayout(layout_field_hbox)
        self.layout_help.addLayout(layout_start_date_hbox)

    def create_decision_table(self):
        self.decision_table = QTableWidget(self)
        self.decision_table.setRowCount(3)
        self.decision_table.setColumnCount(6)  # Columns: Name, C1, C2, C3, C4, C5
        self.decision_table.setHorizontalHeaderLabels(["Name", "C1", "C2", "C3", "C4", "C5"])

        self.layout_table_decision = QVBoxLayout()
        self.layout_table_decision.addWidget(self.decision_table)

    def ui_decision_table_with_weight(self):
        self.decision_table_with_weight = QTableWidget(self)
        self.decision_table_with_weight.setRowCount(3)
        self.decision_table_with_weight.setColumnCount(6)  # Columns: Name, C1, C2, C3, C4, C5
        self.decision_table_with_weight.setHorizontalHeaderLabels(["Name", "C1", "C2", "C3", "C4", "C5"])

        self.layout_table_decision_with_weight = QVBoxLayout()
        self.layout_table_decision_with_weight.addWidget(self.decision_table_with_weight)

    def create_menu(self):
        # Tạo QMenu với các lựa chọn
        self.menu = QMenu()
        for paper in self.controller.papers:
            action = QAction(paper.topic, self)
            action.setData(paper)
            action.triggered.connect(partial(self.combo_box_change, paper))
            self.menu.addAction(action)

    def combo_box_change(self, data: Paper):
        print(f"HanhLT: data name ={data.topic}")
        self.label_name_topic.setText(data.topic)
        self.label_field_name.setText(", ".join(data.field))
        self.label_author_name.setText(", ".join(data.authors))
        self.label_date.setText(data.date)

        list_reviewers = self.controller.filter_researchers(data)
        result = self.controller.calculate_decision_matrix(list_reviewer=list_reviewers, paper=data)
        print(f"HanhLT: result = {result}")
        self.decision_table.setRowCount(len(result))  # Make sure row count matches number of reviewers

        for row_index, (name, criteria) in enumerate(result.items()):
            # Set name
            self.decision_table.setItem(row_index, 0, QTableWidgetItem(name))
            # Set C1 to C5
            for col_index, value in enumerate(criteria):
                self.decision_table.setItem(row_index, col_index + 1, QTableWidgetItem(str(value)))

    def resize_table(self, width):
        self.decision_table_with_weight.setColumnWidth(0, 0.25 * width)  # Name
        self.decision_table_with_weight.setColumnWidth(1, 0.1 * width)  # C1
        self.decision_table_with_weight.setColumnWidth(2, 0.12 * width)  # C2
        self.decision_table_with_weight.setColumnWidth(3, 0.15 * width)  # C3
        self.decision_table_with_weight.setColumnWidth(4, 0.15 * width)  # C4
        self.decision_table_with_weight.setColumnWidth(5, 0.12 * width)  # C5

        self.decision_table.setColumnWidth(0, 0.25 * width)  # Name
        self.decision_table.setColumnWidth(1, 0.1 * width)  # C1
        self.decision_table.setColumnWidth(2, 0.12 * width)  # C2
        self.decision_table.setColumnWidth(3, 0.15 * width)  # C3
        self.decision_table.setColumnWidth(4, 0.15 * width)  # C4
        self.decision_table.setColumnWidth(5, 0.12 * width)  # C5

    def resizeEvent(self, event):
        self.resize_table(self.width()/2)
