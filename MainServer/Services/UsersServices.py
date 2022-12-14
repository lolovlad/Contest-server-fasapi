from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..tables import User, TeamRegistration, ContestRegistration
from ..Models.User import UserPost, UserUpdate, UserBase, UserGetInTeam, TeamUser
from ..Models.Message import StatusUser
from ..database import get_session


class UsersServices:
    def __init__(self, session: Session = Depends(get_session)):
        self.__session: Session = session

    def __get(self, id_user: int):
        user = self.__session.query(User).filter(User.id == id_user).first()
        return user

    def __is_login(self, user: UserBase):
        users = self.__session.query(User).filter(User.login == user.login).first()
        if users:
            return True
        return False

    def get_list_user(self) -> List[User]:
        return self.__session.query(User).all()

    def get_list_in_team_user(self, id_team: int) -> List[User]:
        users = self.__session.query(User).all()
        target_user = []
        for user in users:
            id_teams = list(map(lambda x: x.id_team, user.teams))
            if id_team not in id_teams:
                target_user.append(user)
        return target_user

    def add_user(self, user_data: UserPost) -> User:
        if self.__is_login(user_data):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
        user = User(**user_data.dict())
        user.password = user_data.password
        self.__session.add(user)
        self.__session.commit()
        return user

    def update_user(self, id_user: int, user_data: UserUpdate) -> User:
        user = self.__get(id_user)
        for field, val in user_data:
            if field == "password":
                if len(val) > 0:
                    setattr(user, field, val)
            else:
                setattr(user, field, val)
        self.__session.commit()
        return user

    def delete_user(self, id_user: int):
        user = self.__get(id_user)
        team_reg = self.__session.query(TeamRegistration).filter(TeamRegistration.id_user == id_user).all()
        contest_reg = self.__session.query(ContestRegistration).filter(ContestRegistration.id_user == id_user).all()
        for instance in team_reg + contest_reg:
            self.__session.delete(instance)
        self.__session.delete(user)
        self.__session.commit()
        return user

    def get_list_in_contest_user(self, id_contest: int) -> List[UserGetInTeam]:
        users = self.__session.query(User).all()
        target_user = []
        for user in users:
            id_contests = list(map(lambda x: x.id_contest, user.contests))
            if id_contest not in id_contests:
                teams = list(map(lambda x: TeamUser(id=x.team.id,
                                                    name_team=x.team.name_team), user.teams))
                target_user.append(UserGetInTeam(id=user.id,
                                                 name=user.name,
                                                 sename=user.sename,
                                                 secondname=user.secondname,
                                                 teams=teams))
        return target_user

    def status_user(self, id_contest: int, id_user: int) -> StatusUser:
        contest = self.__session.query(ContestRegistration).filter(ContestRegistration.id_contest == id_contest)\
            .filter(ContestRegistration.id_user == id_user).first()
        return StatusUser(**{"id_user": id_user, "status": contest.state_contest})


