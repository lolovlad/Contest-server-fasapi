from fastapi import Depends
from typing import List
from ..Models.TypeCompilation import TypeCompilationGet
from ..tables import TypeCompilation

from sqlalchemy.orm import Session
from ..database import get_session


class TypeCompilationServices:
    def __init__(self, session: Session = Depends(get_session)):
        self.__session = session

    def get_list_compilation(self) -> List[TypeCompilation]:
        compilation = self.__session.query(TypeCompilation).all()
        return compilation

