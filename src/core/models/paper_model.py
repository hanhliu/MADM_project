import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict
from datetime import date

@dataclass
class Paper:
    id: str = None
    topic: str = None
    field: List[str] = None
    date: date = None
    reviewer_degree_requirement: str = None
    required_reviewer_rating: float = None
    min_reviewers: int = None
    authors: List[str] = None
    numbers_of_published_papers_requirement: int = None
    years_of_experience_requirement: int = None

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        paper = cls()
        paper.topic = data.get("topic")
        paper.field = data.get("field", [])
        paper.date = data.get("date")
        paper.reviewer_degree_requirement = data.get("reviewer_degree_requirement")
        paper.required_reviewer_rating = data.get("required_reviewer_rating")
        paper.min_reviewers = data.get("min_reviewers")
        paper.authors = data.get("authors", [])
        paper.numbers_of_published_papers_requirement = data.get("numbers_of_published_papers_requirement")
        paper.years_of_experience_requirement = data.get("years_of_experience_requirement")
        return paper
