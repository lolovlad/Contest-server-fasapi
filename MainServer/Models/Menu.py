from pydantic import BaseModel
from ..Models.Contest import ContestGet
from typing import List


class Menu(BaseModel):
    state_user: int
    contests: ContestGet
