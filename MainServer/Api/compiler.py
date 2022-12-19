from fastapi import APIRouter, Depends
from typing import List
from ..Models.Compiler import CompilerGet, CompilerPost
from ..Models.User import UserGet, TypeUser
from ..Services.CompilerServices import CompilerServices
from ..Services.LoginServices import get_current_user

router = APIRouter(prefix="/compiler")


@router.get("/", response_model=List[CompilerGet])
def get_compiler(compiler_services: CompilerServices = Depends(),
                 user: UserGet = Depends(get_current_user)):
    if user.type == TypeUser.ADMIN:
        return compiler_services.get_compilers()


@router.post("/", response_model=CompilerGet)
def post_compiler(compiler: CompilerPost,
                  compiler_services: CompilerServices = Depends(),
                  user: UserGet = Depends(get_current_user)):
    if user.type == TypeUser.ADMIN:
        return compiler_services.add_compiler(compiler)
