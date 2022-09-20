from fastapi import APIRouter, Depends, File, UploadFile
from ..Services.TaskServices import TaskServices
from ..Models.Task import TaskGet, TaskPost, TaskDelete, TaskPut


router = APIRouter(prefix="/tasks")


@router.post("/", response_model=TaskGet)
def post_task(task_data: TaskPost, task_services: TaskServices = Depends()):
    return task_services.add_task(task_data)


@router.put("/", response_model=TaskGet)
def put_task(task_data: TaskPut, task_services: TaskServices = Depends()):
    return task_services.update_task(task_data)


@router.delete("/{id_team}", response_model=TaskGet)
def delete_task(id_team: int, task_services: TaskServices = Depends()):
    return task_services.delete_task(id_team)