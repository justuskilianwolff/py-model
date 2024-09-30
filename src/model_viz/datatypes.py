from enum import Enum


class DataType:
    pass


class Undefined(DataType):
    pass


class NoneType(DataType):
    pass


class Integer(DataType):
    pass


class Boolean(DataType):
    pass


class Float(DataType):
    pass


class String(DataType):
    pass


class Enumeration(DataType):
    pass


MATCHING = {
    str(None): NoneType(),
    str(int): Integer(),
    str(float): Float(),
    str(str): String(),
    str(Enum): Enumeration(),
}
