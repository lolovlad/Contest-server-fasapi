from ..Models.Contest import ContestGet, ContestPost, ContestDelete, ContestPutUsers, ContestGetPage
from ..Models.ReportTotal import ReportTotal
from ..Models.Menu import Menu
from fastapi import Depends, APIRouter
from typing import List

from ..Models.User import UserGet, TypeUser
from ..Services.ContestsServices import ContestsServices
from ..Services.LoginServices import get_current_user

router = APIRouter(prefix="/contests")


@router.get("/list_contest", response_model=List[ContestGet])
def get_list_contest(contest_services: ContestsServices = Depends()):
    return contest_services.get_list_contest()


@router.post("/", response_model=ContestGet)
def post_contest(contest_data: ContestPost, contest_services: ContestsServices = Depends(),
                 user: UserGet = Depends(get_current_user)):
    if user.type == TypeUser.ADMIN:
        return contest_services.add_contest(contest_data)


@router.delete("/{id_contest}", response_model=ContestDelete)
def delete_contest(id_contest: int, contest_services: ContestsServices = Depends(),
                   user: UserGet = Depends(get_current_user)):
    if user.type == TypeUser.ADMIN:
        return contest_services.delete_contest(id_contest)


@router.put("/", response_model=ContestGet)
def update_contest(contest_data: ContestGet, contest_services: ContestsServices = Depends(),
                   user: UserGet = Depends(get_current_user)):
    if user.type == TypeUser.ADMIN:
        return contest_services.update_contest(contest_data)


@router.put("/registration_users", response_model=ContestGet)
def registration_users_contest(contest_data: ContestPutUsers, contest_services: ContestsServices = Depends(),
                               user: UserGet = Depends(get_current_user)):
    if user.type == TypeUser.ADMIN:
        return contest_services.add_users_contest(contest_data)


@router.get("/contests_by_user_id/{id_user}", response_model=List[Menu])
def contests_by_user_id(id_user: int, contest_services: ContestsServices = Depends()):
    return contest_services.get_list_contest_by_user_id(id_user)


@router.get("/contest_page/{id_contest}", response_model=ContestGetPage)
def contest_page(id_contest: int, contest_services: ContestsServices = Depends()):
    return contest_services.get_list_page_contest(id_contest)


@router.put("/close_to_user_contest/{id_contest}/{id_user}", response_model=ContestGet)
def close_to_user_contest(id_contest: int, id_user: int, contest_services: ContestsServices = Depends(),
                          user: UserGet = Depends(get_current_user)):
    return contest_services.close_contest_to_user(id_contest, id_user)


@router.get("/report_total/{id_contest}", response_model=List[ReportTotal])
def get_report_total(id_contest: int, contest_services: ContestsServices = Depends()):
    return contest_services.get_report_total(id_contest)