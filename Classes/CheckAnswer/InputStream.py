from ..PathFileDir import PathFileDir
from subprocess import Popen


class InputStream:
    def __init__(self, name_dir):
        self.__name_dir = name_dir

    def start_stream(self, input_data):
        return "\n".join(input_data).encode()