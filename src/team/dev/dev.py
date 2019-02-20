from .enums import *


class Dev:

    def __init__(self, name: str, dev_type: Type):
        self.__name: str = name
        self.__type: Type = dev_type

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> Type:
        return self.__type

    def __str__(self):
        return f"""Developer name: {self.__name}
                  Developer type: {self.__type}"""
