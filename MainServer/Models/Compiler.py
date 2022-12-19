from pydantic import BaseModel


class CompilerBase(BaseModel):
    name_compilation: str
    path_compilation: str
    path_commands: str


class CompilerGet(CompilerBase):
    id: int

    class Config:
        orm_mode = True


class CompilerPost(CompilerBase):
    pass


class CompilerUpdate(CompilerBase):
    pass
