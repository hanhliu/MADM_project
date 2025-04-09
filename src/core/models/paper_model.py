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
    authors: List[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        paper = cls()
        paper.id = data.get("id")
        paper.topic = data.get("topic")
        paper.field = data.get("field", [])
        paper.date = data.get("date")
        paper.reviewer_degree_requirement = data.get("reviewer_degree_requirement")
        paper.authors = data.get("authors", [])
        return paper
