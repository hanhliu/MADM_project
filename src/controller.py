import json
from datetime import datetime

from src.core.models.paper_model import Paper
from src.core.models.reviewer_model import Reviewer
from src.core.utils import jaccard_similarity


class MainController:
    def __init__(self):
        super().__init__()
        self.papers = self.load_papers_from_json()
        self.reviewers = self.load_reviewers_from_json()
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
            c2_degree_match = 1 if reviewer.degree == required_degree else 0

            # C3: Điểm đánh giá trung bình
            c3_rating = reviewer.average_rating

            # C4: Số bài báo đã xuất bản
            c4_published = reviewer.published_papers

            # C5: Số năm kinh nghiệm nghiên cứu
            c5_experience = reviewer.years_of_experience

            decision_matrix[reviewer.name]=([
                c1_field_match,
                c2_degree_match,
                c3_rating,
                c4_published,
                c5_experience
            ])
        print(f"HanhLT: decision_matrix = {decision_matrix}")
        return decision_matrix

    def calcute_decision_matrix_with_weights(self, weights):
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
            if (reviewer.name not in topic.authors and self.is_available(reviewer, topic.date)
                    and any(field in topic.field for field in reviewer.field)):
                filtered_reviewers.append(reviewer)
        return filtered_reviewers