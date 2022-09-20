from fastapi import APIRouter, Depends, Response, status
from typing import List

from ..Models.User import UserGet, UserPost, UserUpdate, UserGetInTeam
from ..Models.Message import StatusUser
from ..Services.UsersServices import UsersServices

router = APIRouter(prefix='/users')


@router.get('/', response_model=List[UserGet])
def get_users(user_services: UsersServices = Depends()):
    return user_services.get_list_user()


@router.get('/status/{id_contest}/{id_user}', response_model=StatusUser)
def get_status_user(id_contest: int, id_user: int, user_services: UsersServices = Depends()):
    return user_services.status_user(id_contest, id_user)


@router.post('/', response_model=UserGet)
def post_user(user_services: UsersServices = Depends(),
              user: UserPost = None):
    print(user)
    return user_services.add_user(user)


@router.put('/', response_model=UserGet)
def put_user(user_data: UserUpdate,
             user_services: UsersServices = Depends()):
    return user_services.update_user(user_data.id, user_data)


@router.delete('/{user_id}', response_model=UserGet)
def delete_user(user_id: int,
                user_services: UsersServices = Depends()):
    return user_services.delete_user(user_id)


@router.get("/in_team/{id_team}", response_model=List[UserGet])
def get_in_team_users(id_team: int, user_services: UsersServices = Depends()):
    return user_services.get_list_in_team_user(id_team)


@router.get("/in_contest/{id_contest}", response_model=List[UserGetInTeam])
def get_in_contest_users(id_contest: int, user_services: UsersServices = Depends()):
    return user_services.get_list_in_contest_user(id_contest)

