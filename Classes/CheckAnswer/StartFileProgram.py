import subprocess
from time import time, sleep
import psutil
import shlex

from .InputData import InputData
from .OutputData import OutputData
from .Compiler import Compiler
from .VirtualEnvironment import VirtualEnvironment
from ..Models.ReportTesting import ReportTesting
from .Grading import Rating


class StartFileProgram:
    def __init__(self, virtual: VirtualEnvironment, input_stream: InputData,
                 output_stream: OutputData, type_compilation: Compiler):
        self.__venv = virtual
        self.__input_stream = input_stream
        self.__output_stream = output_stream
        self.__process = None
        self.__compiler = type_compilation
        self.__garbage_memory = 17  # цифра взятая с неба необходимы тесты на разных платформах

    def __create_sub_proces(self):
        self.__process = psutil.Popen(shlex.split(self.__compiler.command), shell=False, stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.__venv.path_virtual_environment)

    def start_process(self, input_in_process: str, time_out: int) -> ReportTesting:
        input_data = self.__input_stream.start_stream(input_in_process)
        try:
            self.__create_sub_proces()
            memory = []
            start_time = time()
            outs = self.__process.communicate(input=input_data, timeout=time_out * 1000)
            end_time = time() - start_time
            answer = self.__output_stream.read_output(str(outs[0].decode()))
            outSecond = str(outs[1].decode()).replace("\n", "")
            if outSecond.isdigit():
                memory.append(round((int(outSecond) / 2**10), 3))
                errs = ""
            else:
                memory.append(0)
                errs = outSecond
            if len(errs) == 0:
                errs = 0
            elif len(errs) > 0:
                errs = 1
            report = {
                "out": answer,
                "errors": Rating.OK,
                "time": end_time * 1000,
                "memory": [max(memory)]
            }
            report = ReportTesting(**report)
            return report
        except TimeoutError:
            self.__process.kill()
            return ReportTesting(**{
                "out": [],
                "errors": Rating.TIME_LIMIT_EXCEEDED,
                "time": 0 * 1000,
                "memory": [0.0]
            })
        except Exception:
            return ReportTesting(**{
                "out": [],
                "errors": Rating.COMPILATION_ERROR,
                "time": 0 * 1000,
                "memory": [0.0]
            })