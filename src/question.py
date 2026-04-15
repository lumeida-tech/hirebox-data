from dataclasses import dataclass

@dataclass
class Question:
    title: str
    applicant_full_name: str
    number: int
    body: str