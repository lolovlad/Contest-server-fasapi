from pydantic import BaseModel


class BaseTypeCompilation(BaseModel):
    name_compilation: str
    path_compilation: str
    path_commands: str


class TypeCompilationGet(BaseTypeCompilation):
    id: int

    class Config:
        orm_mode = True
