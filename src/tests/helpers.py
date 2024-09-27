import random
import string


class Generator:
    def __init__(self):
        pass

    @staticmethod
    def generate(string_length: int) -> str:
        return str.join("", random.choices(string.ascii_letters, k=string_length)).lower()
