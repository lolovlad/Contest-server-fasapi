from typing import List
from fastapi import Depends, APIRouter

from ..Models.TypeCompilation import TypeCompilationGet
from ..Models.User import UserGet, TypeUser
from ..Services.LoginServices import get_current_user
from ..Services.TypeCompilationServices import TypeCompilationServices


router = APIRouter(prefix="/type_compilation")


@router.get("/", response_model=List[TypeCompilationGet])
def get_type_compilations(type_compilation_service: TypeCompilationServices = Depends(),):
    return type_compilation_service.get_list_compilation()
