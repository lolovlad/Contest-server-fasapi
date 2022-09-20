from fastapi import APIRouter
from .users import router as users_router
from .login import router as login_router
from .educational_organizations import router as educational_organizations_router
from .teams import router as team_router
from .contests import router as contest_router
from .tasks import router as task_router
from .type_compilation import router as type_compilation_router
from .answers import router as answers_router

router = APIRouter()
router.include_router(users_router)
router.include_router(login_router)
router.include_router(educational_organizations_router)
router.include_router(team_router)
router.include_router(contest_router)
router.include_router(task_router)
router.include_router(type_compilation_router)
router.include_router(answers_router)
