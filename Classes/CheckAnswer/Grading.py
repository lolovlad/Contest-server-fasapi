from ..Models.ReportTesting import Rating


class Grading:
    def __init__(self, size_memory):
        self.__size_memory = size_memory

    def grading(self, correct_answer, code_error, time, size_memory):
        if code_error == Rating.COMPILATION_ERROR:
            return Rating.COMPILATION_ERROR

        elif code_error == Rating.WRONG_ANSWER:
            return Rating.WRONG_ANSWER

        elif code_error == Rating.PRESENTATION_ERROR:
            return Rating.PRESENTATION_ERROR

        elif code_error == Rating.TIME_LIMIT_EXCEEDED:
            return Rating.TIME_LIMIT_EXCEEDED

        elif code_error == Rating.OUTPUT_LIMIT_EXCEEDED:
            return Rating.OUTPUT_LIMIT_EXCEEDED

        elif code_error == Rating.OUTPUT_LIMIT_EXCEEDED:
            return Rating.OUTPUT_LIMIT_EXCEEDED

        elif code_error == Rating.PRECOMPILE_CHECK_FAILED:
            return Rating.PRECOMPILE_CHECK_FAILED

        elif code_error == Rating.IDLENESS_LIMIT_EXCEEDED:
            return Rating.IDLENESS_LIMIT_EXCEEDED

        elif size_memory[0] > self.__size_memory:
            return Rating.MEMORY_LIMIT_EXCEEDED

        elif correct_answer:
            return Rating.OK

        elif correct_answer is False:
            return Rating.WRONG_ANSWER




