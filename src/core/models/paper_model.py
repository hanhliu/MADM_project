import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict
from datetime import date

@dataclass
class Paper:
    topic: str = None
    field: List[str] = None
    date: date = None
    reviewer_degree_requirement: str = None
    required_reviewer_rating: float = None
    min_reviewers: int = None
    authors: List[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict):
        data["date"] = date.fromisoformat(data["date"])
        return Paper(**data)
