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
        self.negative_ideal_solution = []
        self.ideal_solution = []
        self.controller = controller
        self.ui_weights()
        self.ui_criteria()
        self.create_decision_table()
        self.ui_decision_table_with_weight()
        self.create_topsis_layout()
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
        font.setPointSize(9)
        layout_1 = QVBoxLayout()
        layout_2 = QVBoxLayout()
        label_tc = QLabel("TIÊU CHÍ ĐÁNH GIÁ")
        label_1 = QLabel("C1. Trùng lĩnh vực nghiên cứu - số lĩnh vực khớp")
        label_2 = QLabel("C2. Bằng cấp phù hợp (=1 nếu đạt)")
        label_3 = QLabel("C3. Điểm đánh giá cao - dùng trực tiếp")
        label_4 = QLabel("C4. Đã xuất bản nhiều bài báo - dùng trực tiếp")
        label_5 = QLabel("C5. Có nhiều năm nghiên cứu - dùng trực tiếp")
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
        push_button.setStyleSheet(f'''
            QPushButton{{
                background-color: lightblue;
                color: black;
                border-radius: 2px;
                padding: 4px 4px 4px 4px;
            }}
        ''')

        push_button.clicked.connect(self.edit_weights_click)

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
        self.top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.top_layout.addLayout(self.layout_help)
        table_layout = QHBoxLayout()
        self.top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        table_layout.addLayout(self.layout_table_decision)
        table_layout.addLayout(self.layout_table_decision_with_weight)
        self.top_layout.addLayout(table_layout)
        self.top_layout.addLayout(self.topsis_layout)

        widget_top = QWidget()
        widget_top.setObjectName("widget_top")
        widget_top.setLayout(self.top_layout)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.addLayout(self.layout_weight, 1)
        layout.addLayout(self.layout_criteria, 1)
        widget.setLayout(layout)
        widget.setObjectName("temp")
        self.setStyleSheet(f'''
            QWidget#temp{{
                border: 1px solid gray
            }}
            QWidget#widget_top{{
                border: 1px solid gray
            }}
        ''')

        self.main_layout.addWidget(widget_top, 10)
        self.main_layout.addWidget(widget, 1)
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

    def create_topsis_layout(self):
        self.topsis_layout = QHBoxLayout()
        push_button = QPushButton("TOPSIS")
        push_button.setStyleSheet(f'''
            QPushButton{{
                background-color: lightblue;
                color: black;
                border-radius: 2px;
                padding: 4px 4px 4px 4px;
            }}
        ''')
        push_button.clicked.connect(self.topsis_clicked)
        push_button.setFixedWidth(100)
        label_idea_solution = QLabel("Giải pháp lý tưởng:")
        label_positive = QLabel("A+ = ")
        label_positive.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label_negative = QLabel("A- = ")
        label_negative.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label_value_positive = QLabel("[]")
        self.label_value_positive.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label_value_negative = QLabel("[]")
        self.label_value_negative.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_positive = QHBoxLayout()
        layout_positive.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_positive.setSpacing(0)
        layout_positive.addWidget(label_positive)
        layout_positive.addWidget(self.label_value_positive)

        layout_negative = QHBoxLayout()
        layout_negative.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_negative.setSpacing(0)
        layout_negative.addWidget(label_negative)
        layout_negative.addWidget(self.label_value_negative)

        layout_solution = QVBoxLayout()
        layout_solution.addWidget(push_button)
        layout_solution.addWidget(label_idea_solution)
        layout_solution.addLayout(layout_positive)
        layout_solution.addLayout(layout_negative)

        # table S+, S-
        self.table_target = QTableWidget()
        self.table_target.setColumnCount(3)  # Columns: "Name", "S+", "S-"
        self.table_target.setHorizontalHeaderLabels(["Name", "S+", "S-"])

        # table C and rank
        self.table_rank = QTableWidget()
        self.table_rank.setColumnCount(3)  # Columns: "W1", "W2", "W3", "W4", "W5"
        self.table_rank.setHorizontalHeaderLabels(["Name", "C", "RANK"])

        self.topsis_layout.addLayout(layout_solution, 3)
        self.topsis_layout.addWidget(self.table_target, 3)
        self.topsis_layout.addWidget(self.table_rank, 3)


    def create_decision_table(self):
        self.decision_table = QTableWidget(self)
        self.decision_table.setRowCount(3)
        self.decision_table.setColumnCount(6)  # Columns: Name, C1, C2, C3, C4, C5
        self.decision_table.setHorizontalHeaderLabels(["Name", "C1", "C2", "C3", "C4", "C5"])
        label = QLabel("Ma trận quyết định:")
        self.layout_table_decision = QVBoxLayout()
        self.layout_table_decision.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_table_decision.setSpacing(2)
        self.layout_table_decision.addWidget(label)
        self.layout_table_decision.addWidget(self.decision_table)

    def ui_decision_table_with_weight(self):
        self.decision_table_with_weight = QTableWidget(self)
        self.decision_table_with_weight.setRowCount(3)
        self.decision_table_with_weight.setColumnCount(6)  # Columns: Name, C1, C2, C3, C4, C5
        self.decision_table_with_weight.setHorizontalHeaderLabels(["Name", "C1", "C2", "C3", "C4", "C5"])
        label = QLabel("Ma trận quyết định đã chuẩn hoá:")
        self.layout_table_decision_with_weight = QVBoxLayout()
        self.layout_table_decision_with_weight.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_table_decision_with_weight.setSpacing(2)
        self.layout_table_decision_with_weight.addWidget(label)
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
        self.calculate_and_update_table(data)

        # clear data
        self.reset_value()

    def reset_value(self):
        self.label_value_negative.setText("[]")
        self.label_value_positive.setText("[]")
        self.table_target.clear()
        self.table_rank.clear()
        self.table_target.setHorizontalHeaderLabels(["Name", "S+", "S-"])
        self.table_rank.setHorizontalHeaderLabels(["Name", "C", "RANK"])

    def calculate_and_update_table(self, data: Paper):
        list_reviewers = self.controller.filter_researchers(data)
        decision_matrix = self.controller.calculate_decision_matrix(list_reviewer=list_reviewers, paper=data)
        print(f"HanhLT: result = {decision_matrix}")
        self.decision_table.setRowCount(len(decision_matrix))  # Make sure row count matches number of reviewers

        for row_index, (name, criteria) in enumerate(decision_matrix.items()):
            # Set name
            self.decision_table.setItem(row_index, 0, QTableWidgetItem(name))
            # Set C1 to C5
            for col_index, value in enumerate(criteria):
                self.decision_table.setItem(row_index, col_index + 1, QTableWidgetItem(str(value)))

        weight_matrix = self.controller.calcute_decision_matrix_with_weights(decision_matrix=decision_matrix,
                                                                             weights=self.controller.weights)
        self.decision_table_with_weight.setRowCount(len(weight_matrix))
        for row_idx, (name, standardize_value) in enumerate(weight_matrix.items()):
            # Set name
            self.decision_table_with_weight.setItem(row_idx, 0, QTableWidgetItem(name))
            # Set C1 to C5
            for col_index, value in enumerate(standardize_value):
                self.decision_table_with_weight.setItem(row_idx, col_index + 1, QTableWidgetItem(str(value)))

    def topsis_clicked(self):
        self.ideal_solution, self.negative_ideal_solution = self.controller.calculate_ideal_solutions()
        self.label_value_positive.setText(', '.join(map(str, self.ideal_solution)))
        self.label_value_negative.setText(', '.join(map(str, self.negative_ideal_solution)))
        distances = self.controller.calculate_distances_to_ideal()
        topsis_scores, topsis_ranking = self.controller.calculate_topsis_scores()

        self.table_target.setRowCount(len(distances))
        for row_idx, (name, dist_dict) in enumerate(distances.items()):
            # Set reviewer name
            self.table_target.setItem(row_idx, 0, QTableWidgetItem(name))
            # Set S+ and S- (ở cột 1 và 2)
            self.table_target.setItem(row_idx, 1, QTableWidgetItem(str(dist_dict['S+'])))
            self.table_target.setItem(row_idx, 2, QTableWidgetItem(str(dist_dict['S-'])))

        # Đặt số dòng = số reviewer đã xếp hạng
        self.table_rank.setRowCount(len(topsis_ranking))
        # Duyệt theo thứ tự xếp hạng
        for row_index, (name, score) in enumerate(topsis_ranking):
            self.table_rank.setItem(row_index, 0, QTableWidgetItem(name))  # Tên reviewer
            self.table_rank.setItem(row_index, 1, QTableWidgetItem(str(score)))  # Chỉ số C
            self.table_rank.setItem(row_index, 2, QTableWidgetItem(str(row_index + 1)))

    def edit_weights_click(self):
        print("show dialog")
        pass

    def resize_table(self, width):
        self.decision_table_with_weight.setColumnWidth(0, 0.25 * width)  # Name
        self.decision_table_with_weight.setColumnWidth(1, 0.1 * width)  # C1
        self.decision_table_with_weight.setColumnWidth(2, 0.12 * width)  # C2
        self.decision_table_with_weight.setColumnWidth(3, 0.15 * width)  # C3
        self.decision_table_with_weight.setColumnWidth(4, 0.15 * width)  # C4
        self.decision_table_with_weight.setColumnWidth(5, 0.12 * width)  # C5
        self.decision_table_with_weight.setFixedHeight(160)

        self.decision_table.setFixedHeight(160)
        self.decision_table.setColumnWidth(0, 0.25 * width)  # Name
        self.decision_table.setColumnWidth(1, 0.1 * width)  # C1
        self.decision_table.setColumnWidth(2, 0.12 * width)  # C2
        self.decision_table.setColumnWidth(3, 0.15 * width)  # C3
        self.decision_table.setColumnWidth(4, 0.15 * width)  # C4
        self.decision_table.setColumnWidth(5, 0.12 * width)  # C5

        self.table_target.setColumnWidth(0, 0.25 * width)
        self.table_target.setColumnWidth(1, 0.19 * width)
        self.table_target.setColumnWidth(2, 0.19 * width)

        self.table_rank.setColumnWidth(0, 0.25 * width)
        self.table_rank.setColumnWidth(1, 0.2 * width)
        self.table_rank.setColumnWidth(2, 0.19 * width)

    def resizeEvent(self, event):
        self.resize_table(self.width()/2)
