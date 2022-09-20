from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from ..Models.UserLogin import UserLogin
from ..Models.Message import Message
from ..Models.User import UserGet
from ..Services.LoginServices import LoginServices

router = APIRouter(prefix="/login")


@router.get("/", response_model=UserGet, responses={status.HTTP_406_NOT_ACCEPTABLE: {"model": Message}})
def loggin(login: str = None,
           password: str = None,
           login_services: LoginServices = Depends()):
    user = login_services.login_user(UserLogin(login=login,
                                               password=password))
    if user:
        return user
    else:
        return JSONResponse(content={"message": "неправильный логи или пароль"},
                            status_code=status.HTTP_406_NOT_ACCEPTABLE)