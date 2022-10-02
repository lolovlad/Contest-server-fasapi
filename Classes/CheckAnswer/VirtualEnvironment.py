from ..PathExtend import PathExtend
from pathlib import Path
from os import environ, getcwd, chdir


class VirtualEnvironment:
    def __init__(self):
        self.__name_folder: str = PathExtend.create_folder_name()
        self.__path_virtual_environment: PathExtend = PathExtend("Answers", "virtual_environment", self.__name_folder)
        self.__work_folder = getcwd()
        self.__path_file_answer = None

    @property
    def path_file_answer(self):
        return str(self.__path_file_answer)

    @property
    def path_virtual_environment(self):
        return str(self.__path_virtual_environment)

    @property
    def name_folder(self):
        if self.__name_folder is None:
            raise EOFError("not creating virtual folder")
        return self.__name_folder

    def create_virtual_folder(self):
        self.__path_virtual_environment.create_folder()
        self.__path_virtual_environment.create_file("input.txt")
        self.__path_virtual_environment.create_file("output.txt")

    def destruction_virtual_folder(self):
        self.__path_virtual_environment.delete_dir()

    def move_answer_file_to_virtual_environment(self, path_file: PathExtend):
        file = path_file.name_file()
        path_file_program = PathExtend(self.__path_virtual_environment.abs_path(), file)
        path_file.move_file(path_file_program)
        self.__path_file_answer = path_file_program
