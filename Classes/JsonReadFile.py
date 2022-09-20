import json
from pathlib import Path
from MainServer.settings import settings


class JsonFileParser:
    def __init__(self, configuration_file_name: str = ""):
        self.__name_dir: str = settings.files
        dir_path: Path = Path(Path(__file__).parent).parent
        self.__path: Path = Path(dir_path,  self.__name_dir, configuration_file_name)
        self.__config: dict = {}

    def load(self, model: any):
        with open(self.__path, "r") as read_file:
            self.__config = json.load(read_file)
            deserializer_model = model(**self.__config)
            return deserializer_model

    def save(self):
        with open(self.__path, 'w') as outfile:
            json.dump(self.__config, outfile)