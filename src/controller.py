import json
import os
import uuid
from datetime import datetime

import numpy as np
from PySide6.QtCore import Signal, QObject

from src.core.database_local.database_manager import DatabaseManager
from src.core.models.paper_model import Paper
from src.core.models.reviewer_model import Reviewer
from src.core.utils import jaccard_similarity, normalize_decision_matrix, normalize_and_weight_matrix, ItemType


class MainController(QObject):
    signal_change_data = Signal(tuple)
    def __init__(self):
        super().__init__()
        # Tạo instance Singleton
        self.db_manager = DatabaseManager()
        self.papers = []
        self.reviewers = []
        self.distances = {}
        self.topsis_scores = {}
        self.topsis_ranking = None
        self.negative_ideal_solution = []
        self.ideal_solution = []
        self.weighted_matrix = None

        # self.papers = self.load_papers_from_json()
        # self.reviewers = self.load_reviewers_from_json()
        if os.path.exists("madm.db"):
            self.papers = self.db_manager.getAllFromDatabase(ItemType.PAPER.value)
            self.reviewers = self.db_manager.getAllFromDatabase(ItemType.REVIEWER.value)
        else:
            self.load_and_save_reviewer_to_db()
            self.load_and_save_paper_to_db()

        self.list_field = self.get_all_topic_and_user_fields()
        self.list_degree = self.get_all_reviewer_degrees()

        print("List field:", self.list_field)
        print("List degree:", self.list_degree)
        self.weights = [0.3, 0.1, 0.2, 0.1, 0.1]

    def calculate_decision_matrix(self, list_reviewer=None, paper=None):
        decision_matrix = {}

        paper_fields = set(paper.field)
        required_degree = paper.reviewer_degree_requirement
        for reviewer in list_reviewer:
            # C1: Trùng lĩnh vực nghiên cứu (Jaccard - số lĩnh vực khớp)
            reviewer_fields = set(reviewer.field)
            # c1_field_match = jaccard_similarity(reviewer_fields, paper_fields)
            c1_field_match = len(paper_fields.intersection(reviewer_fields))

            # C2: Bằng cấp phù hợp
            c2_degree_match = 1 if self.is_degree_acceptable(reviewer.degree, required_degree) else 0

            # C3: Điểm đánh giá trung bình
            c3_rating = reviewer.average_rating

            # C4: Số bài báo đã xuất bản
            c4_published = reviewer.published_papers

            # C5: Số năm kinh nghiệm nghiên cứu
            c5_experience = reviewer.years_of_experience

            decision_matrix[reviewer.name] = ([
                c1_field_match,
                c2_degree_match,
                c3_rating,
                c4_published,
                c5_experience
            ])
        return decision_matrix

    def calcute_decision_matrix_with_weights(self, decision_matrix, weights):
        """
        weights: List of 5 weights [w1, w2, w3, w4, w5]
        """

        reviewers = list(decision_matrix.keys())
        matrix_values = list(decision_matrix.values())

        weighted_matrix = normalize_and_weight_matrix(matrix_values, np.array(weights))

        # Gán lại từng reviewer với vector đã chuẩn hóa và nhân trọng số
        self.weighted_matrix = {
            reviewers[i]: [round(x, 4) for x in weighted_matrix[i]]
            for i in range(len(reviewers))
        }

        return self.weighted_matrix

    def calculate_ideal_solutions(self):
        """
        Tính giải pháp lý tưởng A+ và phản lý tưởng A- từ weighted_matrix
        """
        if not hasattr(self, 'weighted_matrix'):
            print("No weighted matrix found.")
            return

        matrix = np.array(list(self.weighted_matrix.values()), dtype=float)

        # Ideal (best) and Negative-Ideal (worst) solutions
        ideal_solution = np.max(matrix, axis=0)
        negative_ideal_solution = np.min(matrix, axis=0)

        # Làm tròn
        self.ideal_solution = [round(x, 4) for x in ideal_solution]
        self.negative_ideal_solution = [round(x, 4) for x in negative_ideal_solution]

        return self.ideal_solution, self.negative_ideal_solution

    def calculate_distances_to_ideal(self):
        """
        Tính khoảng cách S+ và S- từ từng reviewer đến giải pháp lý tưởng và phản lý tưởng
        """
        if not hasattr(self, 'weighted_matrix') or not hasattr(self, 'ideal_solution') or not hasattr(self,
                                                                                                      'negative_ideal_solution'):
            print("Missing required data for distance calculation.")
            return

        matrix = np.array(list(self.weighted_matrix.values()), dtype=float)
        ideal = np.array(self.ideal_solution)
        negative_ideal = np.array(self.negative_ideal_solution)

        s_plus = np.linalg.norm(matrix - ideal, axis=1)
        s_minus = np.linalg.norm(matrix - negative_ideal, axis=1)

        reviewers = list(self.weighted_matrix.keys())
        self.distances = {
            reviewers[i]: {
                'S+': round(s_plus[i], 4),
                'S-': round(s_minus[i], 4)
            }
            for i in range(len(reviewers))
        }
        return self.distances

    def calculate_topsis_scores(self):
        """
        Tính chỉ số tương tự C cho mỗi reviewer và xếp hạng
        """
        if not hasattr(self, 'distances'):
            print("Distances not calculated.")
            return

        self.topsis_scores = {}
        for name, dist in self.distances.items():
            s_plus = dist['S+']
            s_minus = dist['S-']
            if s_plus + s_minus == 0:
                score = 0
            else:
                score = s_minus / (s_plus + s_minus)
            self.topsis_scores[name] = round(score, 4)

        # Sắp xếp theo điểm C giảm dần
        self.topsis_ranking = sorted(self.topsis_scores.items(), key=lambda x: x[1], reverse=True)
        return self.topsis_scores, self.topsis_ranking

    # Hàm kiểm tra tính khả dụng
    from datetime import datetime

    def is_available(self, researcher, event_date):
        try:
            # event_date_str is a string, need to convert it to datetime
            event_date = datetime.strptime(event_date, "%Y-%m-%d")

            for period in researcher.availability:
                # Check if the availability is in 'start_date to end_date' format
                if 'to' in period:
                    start_date_str, end_date_str = period.split(" to ")
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                    if start_date <= event_date <= end_date:
                        return True
                else:
                    # If it's a single date, check if the event_date matches
                    single_date = datetime.strptime(period, "%Y-%m-%d")
                    if single_date == event_date:
                        return True

            return False
        except ValueError as e:
            print(f"Date format error: {e}")
            return False

    # Lọc các nhà nghiên cứu phù hợp
    def filter_researchers(self, topic: Paper):
        """Loại theo ràng buộc về nguyên tắc đồng tác giả, thời gian rảnh và lĩnh vực nghiên cứu"""
        filtered_reviewers = []
        for reviewer in self.reviewers:
            if (reviewer.name not in topic.authors and self.is_available(reviewer, topic.date)
                    and any(field in topic.field for field in reviewer.field)):
                filtered_reviewers.append(reviewer)
        return filtered_reviewers

    def is_degree_acceptable(self, reviewer_degree, required_degree):
        degree_order = {
            "Master’s": 1,
            "PhD": 2,
            "D.Sc.": 3
        }

        reviewer_level = degree_order.get(reviewer_degree, 0)
        required_level = degree_order.get(required_degree, 0)

        return reviewer_level >= required_level

    def get_data_and_update_ui(self):
        self.papers = self.db_manager.getAllFromDatabase(ItemType.PAPER.value)
        self.reviewers = self.db_manager.getAllFromDatabase(ItemType.REVIEWER.value)
        self.signal_change_data.emit((self.papers, self.reviewers))

    # ADD DATA TO DB
    def add_topic(self, topic: Paper):
        """
        Thêm đề tài vào danh sách và lưu vào cơ sở dữ liệu
        """
        # Kiểm tra xem đề tài đã tồn tại chưa
        for paper in self.papers:
            if paper.topic == topic.topic:
                print("Đề tài đã tồn tại trong danh sách.")
                return

        # Thêm đề tài mới vào danh sách
        self.papers.append(topic)
        self.db_manager.addToDatabase(ItemType.PAPER.value, topic)
        print("Đề tài đã được thêm thành công.")
        self.get_data_and_update_ui()

    def add_reviewer(self, reviewer: Reviewer):
        """
        Thêm nhà nghiên cứu vào danh sách và lưu vào cơ sở dữ liệu
        """
        # Kiểm tra xem nhà nghiên cứu đã tồn tại chưa
        for existing_reviewer in self.reviewers:
            if existing_reviewer.name == reviewer.name:
                print("Reviewer đã tồn tại trong danh sách.")
                return

        # Thêm nhà nghiên cứu mới vào danh sách
        self.reviewers.append(reviewer)
        self.db_manager.addToDatabase(ItemType.REVIEWER.value, reviewer)
        print("Reviewer đã được thêm thành công.")
        self.get_data_and_update_ui()

    def generate_paper_id(self):
        # using uuid
        return str(uuid.uuid4())

    # GET DATA FROM LIST
    def get_all_topic_and_user_fields(self):
        fields = set()

        def process_field(field_data):
            result = []
            if isinstance(field_data, str):
                result = [f.strip() for f in field_data.split(',') if f.strip()]
            elif isinstance(field_data, list):
                result = [f.strip() for f in field_data if isinstance(f, str) and f.strip()]
            return result

        for paper in self.papers:
            for field in process_field(paper.field):
                fields.add(field)

        for reviewer in self.reviewers:
            for field in process_field(reviewer.field):
                fields.add(field)

        return sorted(fields)  # hoặc list(fields) nếu không cần sắp xếp

    def get_all_reviewer_degrees(self):
        return list(set(reviewer.degree for reviewer in self.reviewers if reviewer.degree))

    # ADD DATA TO DATABASE
    def load_and_save_paper_to_db(self):
        self.papers = self.load_papers_from_json()

        for paper in self.papers:
            self.db_manager.addToDatabase(ItemType.PAPER.value, paper)
            pass

    def load_and_save_reviewer_to_db(self):
        self.reviewers = self.load_reviewers_from_json()

        for reviewer in self.reviewers:
            self.db_manager.addToDatabase(ItemType.REVIEWER.value, reviewer)
            pass

    def load_papers_from_json(self):
        try:
            with open("src/core/json/papers.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            # Convert JSON data to Paper objects
            papers = [Paper.from_dict(paper) for paper in data["conferences"]]
            return papers
        except FileNotFoundError:
            print("Không tìm thấy file papers.json")
            return []
        except json.JSONDecodeError:
            print("Lỗi định dạng JSON trong file papers.json")
            return []

    def load_reviewers_from_json(self):
        with open("src/core/json/reviewers.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # Convert JSON data to Paper objects
        reviewers = [Reviewer.from_dict(paper) for paper in data["researchers"]]
        return reviewers
