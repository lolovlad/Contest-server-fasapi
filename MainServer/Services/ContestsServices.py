from fastapi import Depends, HTTPException
from ..Models.Contest import ContestGet, ContestPost, ContestDelete, UserContest, ContestPutUsers, \
    ContestGetPage, TaskPage, TypeContest
from ..Models.ReportTotal import ReportTotal
from ..Models.Menu import Menu
from ..Models.Task import TaskPost, TaskGet
from typing import List

from sqlalchemy.orm import Session
from ..tables import Contest, ContestRegistration, User, Task, Answer, Team
from ..database import get_session
from Classes.PathExtend import PathExtend
from Classes.JsonView import JsonView

from datetime import timedelta


class ContestsServices:
    def __init__(self, session: Session = Depends(get_session)):
        self.__session: Session = session
        self.__time_zone = timedelta(hours=4)

    def __get_by_id(self, id_contest: int) -> Contest:
        return self.__session.query(Contest).filter(Contest.id == id_contest).first()

    def __get_reg_users(self, id_contest: int) -> List[ContestRegistration]:
        users = self.__session.query(ContestRegistration).filter(ContestRegistration.id_contest == id_contest).all()
        return users

    def __convert_contest(self, contest: Contest) -> ContestGet:
        users = list(map(lambda x: UserContest(id=x.user.id,
                                               name=x.user.name,
                                               sename=x.user.sename,
                                               secondname=x.user.secondname), contest.users))
        tasks = list(map(lambda x: TaskGet(id=x.id,
                                           id_contest=x.id_contest,
                                           time_work=x.time_work,
                                           size_raw=x.size_raw,
                                           type_input=x.type_input,
                                           type_output=x.type_output,
                                           name_task=x.name_task,
                                           description=x.description,
                                           description_input=x.description_input,
                                           description_output=x.description_output,
                                           type_task=x.type_task,
                                           number_shipments=x.number_shipments,
                                           path_test_file=x.path_test_file), contest.tasks))
        contest_reg = ContestGet(id=contest.id,
                                 users=users,
                                 name_contest=contest.name_contest,
                                 datetime_start=contest.datetime_start,
                                 datetime_end=contest.datetime_end,
                                 datetime_registration=contest.datetime_registration,
                                 type=contest.type,
                                 state_contest=contest.state_contest,
                                 tasks=tasks)
        return contest_reg

    def get_list_contest(self) -> List[ContestGet]:
        contests = self.__session.query(Contest).all()
        contest_reg = []
        for contest in contests:
            contest_reg.append(self.__convert_contest(contest))
        return contest_reg

    def get_list_contest_by_user_id(self, id_user: int) -> List[Menu]:
        contests_reg = self.__session.query(ContestRegistration).filter(ContestRegistration.id_user == id_user).all()
        menu_target = []
        for contest_reg in contests_reg:
            contest = self.__convert_contest(contest_reg.contest)
            menu_target.append(Menu(**{"state_user": contest_reg.state_contest, "contests": contest}))
        return menu_target

    def get_list_page_contest(self, id_contest: int) -> ContestGetPage:
        contest = self.__get_by_id(id_contest)
        tasks_page = []

        for task in contest.tasks:
            view = JsonView(task.path_test_file)
            view.generate_view()
            tasks_page.append(TaskPage(id=task.id,
                                       id_contest=task.id_contest,
                                       time_work=task.time_work,
                                       size_raw=task.size_raw,
                                       type_input=task.type_input,
                                       type_output=task.type_output,
                                       name_task=task.name_task,
                                       description=task.description,
                                       description_input=task.description_input,
                                       description_output=task.description_output,
                                       type_task=task.type_task,
                                       number_shipments=task.number_shipments,
                                       task_view=view.view))
        contest_reg = ContestGetPage(id=contest.id,
                                     name_contest=contest.name_contest,
                                     datetime_start=contest.datetime_start,
                                     datetime_end=contest.datetime_end,
                                     datetime_registration=contest.datetime_registration,
                                     type=contest.type,
                                     state_contest=contest.state_contest,
                                     tasks=tasks_page)
        return contest_reg

    def add_contest(self, contest_data: ContestPost) -> ContestGet:
        contest = Contest(name_contest=contest_data.name_contest,
                          datetime_start=contest_data.datetime_start + self.__time_zone,
                          datetime_end=contest_data.datetime_end + self.__time_zone,
                          type=contest_data.type,
                          state_contest=contest_data.state_contest)

        self.__session.add(contest)
        self.__session.commit()
        contest = self.__convert_contest(contest)
        return contest

    def add_users_contest(self, contest_data: ContestPutUsers) -> ContestGet:
        contest = self.__get_by_id(contest_data.id)
        users = self.__get_reg_users(contest_data.id)
        for user in users:
            self.__session.delete(user)
        for user in contest_data.users:
            contest_reg = ContestRegistration(id_user=user.id,
                                              id_contest=contest.id,
                                              id_team=user.id_team)
            self.__session.add(contest_reg)
        self.__session.commit()
        contest = self.__convert_contest(contest)
        return contest

    def delete_contest(self, id_contest: int) -> ContestDelete:
        contest = self.__get_by_id(id_contest)
        users = self.__get_reg_users(id_contest)
        answers = self.__session.query(Answer).filter(Answer.id_contest == id_contest).all()
        for user in users:
            self.__session.delete(user)

        for task in contest.tasks:
            path_file = PathExtend(task.path_test_file)
            path_file.delete_file()
            self.__session.delete(task)

        for answer in answers:
            path_file_test = PathExtend(answer.path_test_file)
            path_file_programme_file = PathExtend(answer.path_programme_file)
            path_file_test.delete_file()
            path_file_programme_file.delete_file()
            self.__session.delete(answer)

        self.__session.delete(contest)
        self.__session.commit()

        contest = ContestDelete(id=contest.id,
                                name_contest=contest.name_contest,
                                datetime_start=contest.datetime_start,
                                datetime_end=contest.datetime_end,
                                datetime_registration=contest.datetime_registration,
                                type=contest.type,
                                state_contest=contest.type)
        return contest

    def update_contest(self, contest_data: ContestGet) -> ContestGet:
        contest = self.__get_by_id(contest_data.id)
        users = self.__get_reg_users(contest_data.id)
        for user in users:
            self.__session.delete(user)

        for field, val in contest_data:
            if field in ("name_contest", "state_contest"):
                setattr(contest, field, val)
            elif field in ("datetime_start", "datetime_end"):
                setattr(contest, field, val + self.__time_zone)
        for user in contest_data.users:
            user_reg = ContestRegistration(id_user=user.id,
                                           id_contest=contest.id)
            self.__session.add(user_reg)

        self.__session.commit()
        contest = self.__get_by_id(contest.id)
        contest = self.__convert_contest(contest)
        return contest

    def close_contest_to_user(self, id_contest: int, id_user: int) -> ContestGet:
        contest = self.__session.query(ContestRegistration).filter(ContestRegistration.id_contest == id_contest)\
            .filter(ContestRegistration.id_user == id_user).first()

        contest.state_contest = 2
        self.__session.commit()
        contest = self.__session.query(Contest).filter(Contest.id == id_contest).first()
        return self.__convert_contest(contest)

    def get_report_total(self, id_contest: int) -> List[ReportTotal]:
        contest = self.__session.query(Contest).filter(Contest.id == id_contest).first()
        reports = []
        if contest.type != TypeContest.OLIMPIADA:
            contest_reg = self.__session.query(ContestRegistration).filter(ContestRegistration.id_contest == id_contest).all()
            id_teams = set([team.id_team for team in contest_reg])
            for id_team in id_teams:
                totals = {}
                sum_point_one = 0
                team_all = self.__session.query(Team).filter(Team.id == id_team).first()
                for task in contest.tasks:
                    answers = self.__session.query(
                        Answer
                    ).filter(
                        Answer.id_task == task.id
                    ).filter(
                        Answer.id_team == id_team
                    ).all()
                    if len(answers) > 0:
                        answer_task = list(sorted(answers, key=lambda x: x.points, reverse=True))[0]
                        totals[task.id] = {"points": answer_task.points}
                        sum_point_one += answer_task.points
                    else:
                        totals[task.id] = {"points": 0}
                response = {
                    "name_team": team_all.name_team,
                    "total": totals,
                    "sum_point": sum_point_one,
                    "name_contest": contest.name_contest,
                    "type_contest": contest.type
                }
                reports.append(ReportTotal(**response))
        else:
            for user in contest.users:
                totals = {}
                sum_point_one = 0
                for task in contest.tasks:
                    answers = self.__session.query(
                        Answer
                    ).filter(
                        Answer.id_task == task.id
                    ).filter(
                        Answer.id_user == user.user.id
                    ).all()
                    if len(answers) > 0:
                        answer_task = list(sorted(answers, key=lambda x: x.points, reverse=True))[0]
                        totals[task.id] = {"points": answer_task.points}
                        sum_point_one += answer_task.points
                    else:
                        totals[task.id] = {"points": 0}
                response = {
                    "name_user": f"{user.user.sename} {user.user.name} {user.user.secondname}",
                    "total": totals,
                    "sum_point": sum_point_one,
                    "name_contest": contest.name_contest,
                    "type_contest": contest.type
                }
                reports.append(ReportTotal(**response))
        return reports


