import json
from pathlib import Path
from MainServer.settings import settings
from .PathExtend import PathExtend


class JsonFileParser:
    def __init__(self, configuration_file_name: str = ""):
        self.__path: PathExtend = PathExtend(configuration_file_name)
        self.__config: dict = {}

    def load(self, model: any):
        with open(self.__path.abs_path(), "r") as read_file:
            self.__config = json.load(read_file)
            deserializer_model = model(**self.__config)
            return deserializer_model

    def save(self):
        with open(self.__path.abs_path(), 'w') as outfile:
            json.dump(self.__config, outfile)