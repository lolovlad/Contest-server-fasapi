from fastapi import Depends
from sqlalchemy.orm import Session

from ..tables import User
from ..Models.UserLogin import UserLogin
from ..database import get_session


class LoginServices:
    def __init__(self, session: Session = Depends(get_session)):
        self.__session = session

    def __get(self, login_user: str) -> User:
        user = self.__session.query(User).filter(User.login == login_user).first()
        return user

    def login_user(self, user_login: UserLogin) -> User:
        user = self.__get(user_login.login)
        if user:
            if user.check_password(user_login.password):
                return user