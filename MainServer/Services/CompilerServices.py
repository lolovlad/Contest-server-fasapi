from fastapi import Depends
from ..database import get_session
from typing import List

from ..Models.Compiler import CompilerGet, CompilerPost, CompilerUpdate
from ..tables import TypeCompilation
from sqlalchemy.orm import Session


class CompilerServices:
    def __init__(self, session: Session = Depends(get_session)):
        self.__session: Session = session

    def __get_compilers(self) -> List[TypeCompilation]:
        return self.__session.query(TypeCompilation).all()

    def get_compilers(self) -> List[TypeCompilation]:
        return self.__get_compilers()

    def add_compiler(self, compiler: CompilerPost) -> TypeCompilation:
        compiler_add = TypeCompilation(**compiler.dict())
        self.__session.add(compiler_add)
        self.__session.commit()
        return compiler_add
