from ..CheckAnswer.InputStream import InputStream
from ..CheckAnswer.FileStream import FileStream


class InputData:
    def __init__(self, path):
        self.__file_data = FileStream(path)
        self.__input_data = InputStream(path)
        self.__input_stream = None

    def creating_input_data(self, type_data):
        if type_data == 1:
            self.__input_stream = self.__input_data
        elif type_data == 2:
            self.__input_stream = self.__file_data

    def start_stream(self, input_data):
        return self.__input_stream.start_stream(input_data)


