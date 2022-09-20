from ..PathFileDir import PathFileDir
from pathlib import Path
from os import environ, getcwd, chdir


class VirtualEnvironment:
    def __init__(self):
        self.__name_folder = PathFileDir.genera_name_folder()
        self.__path_virtual_environment = PathFileDir.abs_path(f"Answers/virtual_environment/{self.__name_folder}")
        self.__work_folder = getcwd()
        self.__path_file_answer = None

    @property
    def path_file_answer(self):
        return str(self.__path_file_answer).replace("\\", "/")

    @property
    def path_virtual_environment(self):
        return str(self.__path_virtual_environment).replace("\\", "/")

    @property
    def name_folder(self):
        if self.__name_folder is None:
            raise EOFError("not creating virtual folder")
        return self.__name_folder

    def create_virtual_folder(self):
        PathFileDir.create_folders(self.__path_virtual_environment)
        open(f"{self.__path_virtual_environment}/input.txt", 'w').close()
        open(f"{self.__path_virtual_environment}/output.txt", 'w').close()

    def destruction_virtual_folder(self):
        PathFileDir.delete_dir(PathFileDir.str_to_abs_path(self.__path_virtual_environment))

    def move_answer_file_to_virtual_environment(self, path_file):
        file = PathFileDir.name_file_to_dir(path_file)
        path_file_program = Path(str(self.__path_virtual_environment) + f"\\{file}")
        PathFileDir.move_file(path_file, path_file_program)
        self.__path_file_answer = path_file_program
