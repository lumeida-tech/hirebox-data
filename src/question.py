from dataclasses import dataclass

@dataclass
class Question:
    title: str
    number: int
    body: str