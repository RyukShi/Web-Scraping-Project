import os

from time import sleep
from random import uniform
from json import dump, load


def chill(mult: float = 1.0):
    """ Chill for a while """
    sleep(uniform(mult * 1.5, mult * 2.5))


def join_path(path: str, folder: str, filename: str) -> str:
    """ Join path and filename """
    return os.path.join(path, folder, filename)


def is_exists(path: str) -> bool:
    """ Return True if file exists, False otherwise """
    return os.path.isfile(path)


def get_size(path: str) -> int:
    """ Return the size of a file """
    return os.path.getsize(path)


def is_valid_file(path: str) -> bool:
    return is_exists(path) and get_size(path) > 0


def deserialize_data(path: str):
    """ Deserialize json data from file """
    with open(path, 'r', encoding='utf-8') as file:
        try:
            return load(file)
        except ValueError as e:
            print(f"Failed to load json data from file, Error: {e}")
            return None


def serialize_data(path: str, data: dict) -> bool:
    """ Serialize python dict to json format into a file """
    with open(path, 'w', encoding='utf-8') as file:
        try:
            dump(data, file, indent=4)
            return True
        except ValueError as e:
            print(f"Failed to dump data into file, Error: {e}")
            return False
