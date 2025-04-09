import json
from datetime import datetime

import numpy as np

from src.core.database_local.database_manager import DatabaseManager
from src.core.models.paper_model import Paper
from src.core.models.reviewer_model import Reviewer
from src.core.utils import jaccard_similarity, normalize_decision_matrix, normalize_and_weight_matrix, ItemType


class MainController:
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
        self.papers = self.load_papers_from_json()
        self.reviewers = self.load_reviewers_from_json()
        # self.load_and_save_reviewer_to_db()
        # self.load_and_save_paper_to_db()
        self.papers = self.db_manager.getAllFromDatabase(ItemType.PAPER.value)
        self.reviewers = self.db_manager.getAllFromDatabase(ItemType.REVIEWER.value)
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
        print(f"HanhLT: decision_matrix in controller = {decision_matrix}")
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

        print("HanhLT: weighted_matrix =", self.weighted_matrix)
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

        print(f"HanhLT: A+ (Ideal) = {self.ideal_solution}")
        print(f"HanhLT: A- (Negative Ideal) = {self.negative_ideal_solution}")

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

        print(f"HanhLT: Distances = {self.distances}")
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
            print(f"s_minus = {s_minus}   s_plus={s_plus}")
            if s_plus + s_minus == 0:
                score = 0
            else:
                score = s_minus / (s_plus + s_minus)
            self.topsis_scores[name] = round(score, 4)

        # Sắp xếp theo điểm C giảm dần
        self.topsis_ranking = sorted(self.topsis_scores.items(), key=lambda x: x[1], reverse=True)

        print(f"HanhLT: TOPSIS Scores = {self.topsis_scores}")
        print(f"HanhLT: Ranking = {self.topsis_ranking}")
        return self.topsis_scores, self.topsis_ranking

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

    # Hàm kiểm tra tính khả dụng
    def is_available(self, researcher, event_date):
        try:
            # event_date_str là chuỗi, cần chuyển sang datetime
            event_date = datetime.strptime(event_date, "%Y-%m-%d")
            for period in researcher.availability:
                start_date_str, end_date_str = period.split(" to ")
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                if start_date <= event_date <= end_date:
                    return True
            return False
        except ValueError as e:
            print(f"Lỗi định dạng ngày: {e}")
            return False

    # Lọc các nhà nghiên cứu phù hợp
    def filter_researchers(self, topic: Paper):
        """Loại theo ràng buộc về nguyên tắc đồng tác giả, thời gian rảnh và lĩnh vực nghiên cứu"""
        filtered_reviewers = []
        for reviewer in self.reviewers:
            print(f"HanhLT: self.is_available(reviewer, topic.date) = {self.is_available(reviewer, topic.date)}")
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

    def load_and_save_paper_to_db(self):
        self.papers = self.load_papers_from_json()

        for paper in self.papers:
            self.db_manager.addToDatabase(ItemType.PAPER.value, paper)

    def load_and_save_reviewer_to_db(self):
        self.reviewers = self.load_reviewers_from_json()

        for reviewer in self.reviewers:
            self.db_manager.addToDatabase(ItemType.REVIEWER.value, reviewer)
