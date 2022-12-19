from fastapi import Depends, APIRouter
from typing import List

from ..Models.Answer import AnswerGet, AnswerPost
from ..Models.Message import Answers
from Classes.Models.Report import Report
from ..Services.AnswersServices import AnswersServices

from ..Services.LoginServices import get_current_user
from ..Models.User import UserGet


router = APIRouter(prefix="/answers")


@router.get("/package/{id_contest}/{id_user}", response_model=List[AnswerGet])
def get_package(id_contest: int, id_user: int, answers_services: AnswersServices = Depends(),
                user: UserGet = Depends(get_current_user)):
    return answers_services.get_package_answers(id_contest, user.id)


@router.get("/{id_contest}/{id_task}/{id_user}", response_model=Answers)
def get_answers(id_contest: int, id_task: int,
                id_user: int, answers_services: AnswersServices = Depends(),
                user: UserGet = Depends(get_current_user)):
    list_answers = answers_services.get_list_answer(id_contest, id_task, user.id)
    menu = answers_services.max_points_tasks(id_contest, user.id)
    return {"menu": menu, "answers": list_answers}


@router.get("/report/{id_answer}", response_model=Report)
def get_report(id_answer: int, answers_services: AnswersServices = Depends()):
    return answers_services.get_report(id_answer)


@router.post("/", response_model=AnswerGet)
def post_answers(answer_data: AnswerPost, answers_services: AnswersServices = Depends(),
                 user: UserGet = Depends(get_current_user)):
    answer_data.id_user = user.id
    return answers_services.add_answer(answer_data)