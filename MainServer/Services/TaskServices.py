from fastapi import Depends
from typing import List
from sqlalchemy.orm import Session
from Classes.PathFileDir import PathFileDir

from ..Models.Task import TaskGet, TaskPost, TaskDelete, TaskPut
from ..tables import Task
from ..database import get_session


class TaskServices:
    def __init__(self, session: Session = Depends(get_session)):
        self.__session = session

    def __get(self, id_task: int):
        return self.__session.query(Task).filter(Task.id == id_task).first()

    def add_task(self, task_data: TaskPost) -> Task:
        name_json = PathFileDir.create_file_name("json", start_name_file=f"task_test_file_{task_data.name_task}")

        name_json = PathFileDir.abs_path(f"{name_json}")
        PathFileDir.write_file(name_json, task_data.file, "wb")
        task_dict = task_data.dict()
        task_dict["path_test_file"] = str(name_json)
        task_dict.pop("file")
        task = Task(**task_dict)
        self.__session.add(task)
        self.__session.commit()
        return task

    def update_task(self, task_data: TaskPut) -> Task:
        task = self.__get(task_data.id)
        for field, val in task_data:
            if field == "file":
                if len(val) != 0:
                    PathFileDir.write_file(task.path_test_file, task_data.file, "wb")
            else:
                setattr(task, field, val)
        self.__session.commit()
        return task

    def delete_task(self, id_task: int) -> Task:
        task = self.__get(id_task)
        PathFileDir.delete_file(task.path_test_file)
        self.__session.delete(task)
        self.__session.commit()
        return task
