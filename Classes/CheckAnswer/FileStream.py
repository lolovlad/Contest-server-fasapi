from ..PathExtend import PathExtend
from subprocess import Popen


class FileStream:
    def __init__(self, name_dir):
        self.__name_dir = name_dir
        self.__name_file = "input.txt"

    def start_stream(self, input_data):
        path_file = PathExtend(f"{self.__name_dir}/{self.__name_file}")
        path_file.write_file("\n".join(input_data))
        return None