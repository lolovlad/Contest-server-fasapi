from ..PathFileDir import PathFileDir
from subprocess import Popen


class FileStream:
    def __init__(self, name_dir):
        self.__name_dir = name_dir
        self.__name_file = "input.txt"

    def start_stream(self, input_data):
        PathFileDir.write_file(f"{self.__name_dir}/{self.__name_file}", "\n".join(input_data))
        return None