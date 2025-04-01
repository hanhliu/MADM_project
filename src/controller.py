import json
from src.core.models.paper_model import Paper
from src.core.models.reviewer_model import Reviewer


class MainController:
    def __init__(self):
        super().__init__()
        self.papers = self.load_papers_from_json()
        self.reviewers = self.load_reviewers_from_json()


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
