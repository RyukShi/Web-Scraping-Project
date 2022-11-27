import os

from time import sleep
from random import uniform


def chill(mult: float = 1.0):
    """ Chill for a while """
    sleep(uniform(mult * 1.5, mult * 2.5))


def join_path(path: str, folder: str, filename: str) -> str:
    """ Join path and filename """
    return os.path.join(path, folder, filename)


def is_exists(path: str) -> bool:
    """ Return True if file exists, False otherwise """
    return os.path.isfile(path)
