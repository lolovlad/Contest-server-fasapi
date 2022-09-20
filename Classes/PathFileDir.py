from pathlib import Path
from random import choices
import shutil
from string import ascii_letters, digits
import os


class PathFileDir:
    __name_dir = "Files"

    @classmethod
    def abs_path(cls, name_file):
        dir_path = Path(Path(__file__).parent).parent
        return Path(dir_path, cls.__name_dir, name_file)

    @classmethod
    def str_to_abs_path(cls, path_file):
        return Path(path_file)

    @classmethod
    def write_file(cls, path_file: str, write_file, type_file="w"):
        cls.create_folders(path_file)

        with open(path_file, type_file) as file:
            file.write(write_file)

    @classmethod
    def create_folders(cls, path_file):
        folders = str(path_file).split("\\")
        length = len(folders[:-1])
        if "." in folders[-1]:
            length = len(folders[:-1])
        else:
            length = len(folders)
        for folder in range(length):
            cls.__create_folder("/".join(folders[:folder + 1]))

    @classmethod
    def __create_folder(cls, path_folder):
        if not os.path.exists(path_folder):
            os.mkdir(path_folder)

    @classmethod
    def create_file_name(cls, extension: str, size: int = 10, start_name_file: str = "file"):
        st = ascii_letters + digits
        return f"{start_name_file}_{''.join(choices(st, k=size))}.{extension}"

    @classmethod
    def genera_name_folder(cls, size=10):
        st = ascii_letters + digits
        return f"{''.join(choices(st, k=size))}"

    @classmethod
    def translate_name_file(cls, file_name):
        return file_name.translate(cls.__create_tabel())

    @classmethod
    def __create_tabel(cls):
        tabel_letters = "а - a б - b в - v г - g д - d е - e ё - e ж - zh з - z и - i й - i к - k л - l м - m н - n " \
                        "о - o п - p р - r с - s т - t у - u ф - f х - kh ц - ts ч - ch ш - sh щ - shch ы - y ъ - ie " \
                        "э - e ю - iu я - ia"
        tabel_letters = tabel_letters.replace(" - ", "@")
        tabel_letters = tabel_letters.split(" ")
        tans = {}
        for letter in tabel_letters:
            letter_translate = letter.split("@")
            tans[letter_translate[0]] = letter_translate[1]
            tans[letter_translate[0].upper()] = letter_translate[1].upper()
            return str.maketrans(tans)

    @classmethod
    def delete_dir(cls, path_dir):
        shutil.rmtree(path_dir)

    @classmethod
    def delete_file(cls, path: str):
        os.remove(path)

    @classmethod
    def move_file(cls, now_path_file, new_path_file):
        shutil.copy2(now_path_file, new_path_file)

    @classmethod
    def name_file_to_dir(cls, path_file):
        path = str(path_file).split("\\")
        if "." in path[-1]:
            return path[-1]
        return None

    @classmethod
    def path_file(cls, path_file):
        path = str(path_file).split("\\")
        return "/".join(path[:-1])