from ..CheckAnswer.OutputStream import OutputStream
from ..CheckAnswer.OutputFileStream import OutputFileStream
from ..PathFileDir import PathFileDir


class OutputData:
    def __init__(self, path):
        self.__input_data = OutputStream(path)
        self.__file_data = OutputFileStream(path)
        self.__output_stream = None

    def creating_output_data(self, type_data):
        if type_data == 1:
            self.__output_stream = self.__input_data
        elif type_data == 2:
            self.__output_stream = self.__file_data

    def read_output(self, input_data):
        return self.__output_stream.read_output(input_data)