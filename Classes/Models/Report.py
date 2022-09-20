from pydantic import BaseModel
from typing import List


class TestReport(BaseModel):
    name_test: str = ""
    point_sum: int = 0
    time: int = 0
    list_test_report: List[str] = []
    state_report: bool = False
    number_test: int = 0
    memory: float = 0


class Report(BaseModel):
    list_report: List[TestReport] = []
