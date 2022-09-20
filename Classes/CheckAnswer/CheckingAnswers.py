import threading
from json import dump, loads

from os import chdir, getcwd
from typing import List

from ..JsonReadFile import JsonFileParser
from MainServer.tables import Answer, Task
from MainServer.database import Session

from ..Models.TaskView import TaskToTest as TaskJson

from ..Models.Report import Report, TestReport
from .InputData import InputData
from .StartFileProgram import StartFileProgram
from .OutputData import OutputData
from .Grading import Grading, Rating
from .VirtualEnvironment import VirtualEnvironment
from .Compiler import Compiler

from ..PathFileDir import PathFileDir


class CreateAnswers:
    def __init__(self):
        self.__pool_answer = []

    def pool_new_answer(self, answer):
        thread_answer = threading.Thread(target=check_answer, args=(answer,))
        thread_answer.start()


class CheckingAnswer:
    def __init__(self, test: TaskJson,
                 type_input: int,
                 type_output: int,
                 timeout: int,
                 size: int,
                 path_compiler: str,
                 file_answer: str):
        self.__test = test
        self.__type_input = type_input
        self.__type_output = type_output
        self.__timeout = timeout
        self.__path_compiler = path_compiler
        self.__file_answer = PathFileDir.str_to_abs_path(file_answer)
        self.__queue = []
        self.__report: Report = Report()
        self.__grading: Grading = Grading(size)
        self.__GRADING: List[str] = ["OK", "CE", "WA", "PE", "TL", "ML", "OL", "RE", "PCF", "IL"]

    def __create_queue(self):
        checkpoint_test = list(filter(lambda x: x.type_test == "test", self.__test.setting_tests))
        main_test = list(filter(lambda x: x.type_test == "main", self.__test.setting_tests))
        self.__queue.insert(0, checkpoint_test[0])
        main_test = list(sorted(main_test, key=lambda x: len(x.settings_test.necessary_test) and sum(x.settings_test.necessary_test)))
        self.__queue += main_test

    def start_examination(self):
        self.__create_queue()

        name_test = 1
        virtual_environment = VirtualEnvironment()
        virtual_environment.create_virtual_folder()
        input_data = InputData(virtual_environment.path_virtual_environment)
        input_data.creating_input_data(self.__type_input)

        output_data = OutputData(virtual_environment.path_virtual_environment)
        output_data.creating_output_data(self.__type_output)

        virtual_environment.move_answer_file_to_virtual_environment(self.__file_answer)

        compiler = Compiler(self.__path_compiler)

        iserro = compiler.run_preprocess({"path_folder": virtual_environment.path_virtual_environment,
                                          "path_file": virtual_environment.path_file_answer,
                                          "name_file": "main.exe"})

        program_file = StartFileProgram(virtual_environment, input_data, output_data, compiler)

        test_report = [TestReport() for _ in range(len(self.__queue))]

        for i, test in enumerate(self.__queue):
            start_checking = []
            test_report[i].point_sum = 0
            test_report[i].time = 0
            if len(test.settings_test.necessary_test) > 0:
                for necessary_test in test.settings_test.necessary_test:
                    start_checking.append(test_report[necessary_test - 1].state_report)
            else:
                start_checking.append(True)

            if all(start_checking) is False:
                test_report[i].state_report = False
                test_report[i].name_test = f"skip test"
                test_report[i].time = 0
                test_report[i].number_test = name_test
                test_report[i].memory = 0
                continue

            test_report[i].state_report = True
            for id_info_test, info_test in enumerate(test.tests):
                information = program_file.start_process(info_test.filling_type_variable, self.__timeout)
                memory = information.memory

                if iserro:
                    information.errors = Rating.COMPILATION_ERROR

                grading = self.__grading.grading(information.out == info_test.answer, information.errors,
                                                 information.time, information.memory)

                test_report[i].list_test_report.append(self.__GRADING[grading.value - 1])

                name_test += 1

                if test.settings_test.check_type == 1:
                    if test_report[i].list_test_report[-1] != "OK":
                        test_report[i].state_report = False
                        test_report[i].name_test = f"test {name_test}"
                        test_report[i].time += 0
                        test_report[i].number_test = name_test
                        test_report[i].memory = round(sum(memory) / len(memory), 3)
                        break
                    else:
                        test_report[i].point_sum += info_test.score
                        test_report[i].number_test = name_test
                        test_report[i].time += int(information.time)
                        test_report[i].memory = round(sum(memory) / len(memory), 3)

            if test_report[i].state_report:
                test_report[i].name_test = "test sucesfull"
                test_report[i].number_test = name_test

        virtual_environment.destruction_virtual_folder()

        return test_report


def create_report_to_answer(report):
    pass


def check_answer(answer_id):
    with Session() as session:
        answer = session.query(Answer).filter(Answer.id == answer_id).first()
        task = session.query(Task).filter(Task.id == answer.id_task).first()

        path_file_test = task.path_test_file

        dir_path_file = PathFileDir.path_file(answer.path_programme_file)

        type_input = task.type_input
        type_output = task.type_output
        timeout = task.time_work
        size = task.size_raw
        test = JsonFileParser(path_file_test).load(TaskJson)
        checking_answer = CheckingAnswer(test, type_input, type_output,
                                         timeout, size, answer.compilation.path_commands, answer.path_programme_file)
        answer_json = checking_answer.start_examination()

        reports = Report()
        reports.list_report = answer_json

        path_file_report = f"{dir_path_file}/{PathFileDir.create_file_name('json')}"

        with open(path_file_report, 'w') as outfile:
            dump(loads(reports.json()), outfile, indent=6)

        answer.path_report_file = str(PathFileDir.abs_path(path_file_report))

        points = 0
        times = 0
        memory = []
        answers = []

        for i in answer_json:

            points += i.point_sum
            answers += i.list_test_report
            times += i.time
            memory.append(i.memory)

        answer.total = "OK"

        for i in answers:
            if i != "OK":
                answer.total = i

        answer.memory_size = round(sum(memory) / len(memory), 3)

        answer.points = points
        answer.number_test = answer_json[-1].number_test
        answer.time = f"{times} ms"
        print(answer.id, "id answer")
        session.commit()


