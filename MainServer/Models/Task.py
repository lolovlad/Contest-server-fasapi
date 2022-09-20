from pydantic import BaseModel
from typing import List
from enum import Enum
from Classes.Models import TaskView


class TypeTask(int, Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    I = 5
    F = 6


class TypeInput(int, Enum):
    STREAM = 1
    FILE = 2


class TypeOutput(int, Enum):
    STREAM = 1
    FILE = 2


class BaseTask(BaseModel):
    id_contest: int
    time_work: int
    size_raw: int
    type_input: TypeInput
    type_output: TypeOutput
    name_task: str
    description: str
    description_input: str
    description_output: str

    type_task: TypeTask
    number_shipments: int


class TaskGet(BaseTask):
    id: int
    path_test_file: str

    class Config:
        orm_mode = True


class TaskPost(BaseTask):
    file: bytes


class TaskPut(BaseTask):
    id: int
    file: bytes = b""
    path_test_file: str


class TaskDelete(BaseTask):
    id: int
    path_test_file: str


class TaskPage(BaseTask):
    id: int
    task_view: TaskView
