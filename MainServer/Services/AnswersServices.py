from fastapi import Depends
from typing import List
from sqlalchemy.orm import Session

from ..Models.Answer import AnswerGet, AnswerPost, UserAnswer, TeamAnswer, TypeCompilationAnswer
from Classes.Models.Report import Report

from ..tables import Answer, Contest, ContestRegistration, Task
from ..database import get_session

from Classes.PathExtend import PathExtend
from Classes.JsonReadFile import JsonFileParser

from Classes.CheckAnswer.CheckingAnswers import CreateAnswers


class AnswersServices:
    def __init__(self, session: Session = Depends(get_session)):
        self.__session = session
        self.__checking_answer: CreateAnswers = CreateAnswers()

    def __convert_answer(self, answer: Answer) -> AnswerGet:
        user = UserAnswer(id=answer.user.id,
                          name=answer.user.name,
                          sename=answer.user.sename,
                          secondname=answer.user.secondname)

        type_compilation = TypeCompilationAnswer(id=answer.compilation.id,
                                                 name_compilation=answer.compilation.name_compilation)

        if answer.team:
            team = TeamAnswer(id=answer.team.id,
                              name_team=answer.team.name_team)
        else:
            team = TeamAnswer()

        answer = AnswerGet(id=answer.id,
                           id_team=answer.id_team,
                           id_user=answer.id_user,
                           id_task=answer.id_task,
                           id_contest=answer.id_contest,
                           type_compiler=answer.type_compiler,
                           total=answer.total,
                           time=answer.time,
                           memory_size=answer.memory_size,
                           number_test=answer.number_test,
                           points=answer.points,
                           user=user,
                           team=team,
                           compilation=type_compilation,
                           date_send=answer.date_send)
        return answer

    def __get_answer_all(self, id_contest: int, id_task: int, id_user: int):
        contest = self.__session.query(ContestRegistration).filter(
            ContestRegistration.id_contest == id_contest
        ).filter(
            ContestRegistration.id_user == id_user
        ).first()
        if contest.id_team:
            answers = self.__session.query(Answer).filter(Answer.id_contest == id_contest). \
                filter(Answer.id_team == contest.id_team).filter(Answer.id_task == id_task).all()
        else:
            answers = self.__session.query(Answer).filter(Answer.id_user == id_user). \
                filter(Answer.id_task == id_task).all()
        return answers

    def max_points_tasks(self, id_contest: int, id_user: int) -> dict:
        contest = self.__session.query(Contest).filter(Contest.id == id_contest).first()
        id_tasks = [task.id for task in contest.tasks]
        menu = {}
        for id_task in id_tasks:
            answer_task = self.__get_answer_all(id_contest, id_task, id_user)
            if len(answer_task) > 0:
                answer_task = list(sorted(answer_task, key=lambda x: x.points, reverse=True))[0]
                menu[id_task] = {"total": answer_task.total,
                                 "points": answer_task.points}
            else:
                menu[id_task] = {"total": "-",
                                 "points": 0}
        return menu

    def get_list_answer(self, id_contest: int, id_task: int, id_user: int) -> List[AnswerGet]:
        answers = self.__get_answer_all(id_contest, id_task, id_user)
        answers_target = []
        for answer in answers:
            answers_target.append(self.__convert_answer(answer))
        return answers_target

    def add_answer(self, answer_data: AnswerPost) -> AnswerGet:
        contest = self.__session.query(ContestRegistration).filter(
            ContestRegistration.id_contest == answer_data.id_contest
        ).filter(
            ContestRegistration.id_user == answer_data.id_user
        ).first()

        name_file = PathExtend.create_file_name(answer_data.extension_file)
        string_path_file = f"Answers/{contest.user.name}_{contest.user.sename}/{name_file}"
        path_file = PathExtend("Answers", f"{contest.user.name}_{contest.user.sename}", name_file)
        path_file.create_folder()
        path_file.write_file(answer_data.file, "wb")

        answer = Answer(id_user=contest.id_user,
                        id_contest=contest.id_contest,
                        id_task=answer_data.id_task,
                        id_team=contest.id_team,
                        path_programme_file=string_path_file,
                        type_compiler=answer_data.type_compilation)

        self.__session.add(answer)
        self.__session.commit()
        self.__checking_answer.pool_new_answer(answer.id)

        return self.__convert_answer(answer)

    def get_report(self, id_answer: int) -> Report:
        answer = self.__session.query(Answer).filter(Answer.id == id_answer).first()
        file_report = answer.path_report_file

        reports = JsonFileParser(file_report).load(Report)
        return reports

    def get_package_answers(self, id_contest: int, id_user: int) -> List[AnswerGet]:
        contest = self.__session.query(ContestRegistration).filter(
            ContestRegistration.id_contest == id_contest and ContestRegistration.id_user == id_user
        ).first()
        if contest.id_team:
            answers = self.__session.query(Answer).filter(Answer.id_contest == id_contest).\
                filter(Answer.id_team == contest.id_team).all()
        else:
            answers = self.__session.query(Answer).filter(Answer.id_user == id_user).all()
        answers_target = []
        for answer in answers:
            answers_target.append(self.__convert_answer(answer))
        return answers_target

