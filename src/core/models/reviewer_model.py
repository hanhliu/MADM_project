from dataclasses import dataclass, asdict
from typing import List, Dict


@dataclass
class Reviewer:
    id: str = None
    name: str = None
    field: List[str] = None
    degree: str = None
    conference_topic: str = None
    average_rating: float = None
    years_of_experience: int = None
    published_papers: int = None
    availability: List[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict):
        return Reviewer(**data)