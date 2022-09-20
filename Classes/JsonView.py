from .JsonReadFile import JsonFileParser
from .Models import TaskToTest


class JsonView:
    def __init__(self, name_json_file: str):
        self.__json_file: JsonFileParser = JsonFileParser(name_json_file)
        self.__model = self.__json_file.load(TaskToTest)
        self.__view = {}

    @property
    def view(self):
        return self.__view

    def generate_view(self):
        example = {"filling_type_variable": [],
                   "answer": []}
        tabel = []
        for test in self.__model.setting_tests:
            str_limited = ", ".join(test.settings_test.limitation_variable)
            #for i, j in [["<=", "&le;"], [">=", "&ge;"], ["<", "&lt;"], [">", "&gt;"], ["=", "&equals;"]]:
            #    str_limited = str_limited.replace(i, j)
            tabel.append({
                "str_limited": str_limited,
                "necessary_test": ", ".join(map(str, test.settings_test.necessary_test))
            })

            if test.type_test == "test":
                for i in test.tests:

                    example["filling_type_variable"].append("\n".join(i.filling_type_variable))
                    example["answer"].append("\n".join(i.answer))

        self.__view = {
            "test": tabel,
            "example": example
        }
        print(example)

