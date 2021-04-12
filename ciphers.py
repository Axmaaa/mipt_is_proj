"""Gets a cipher from an algorithm."""

import enum


class AlgEnum(enum.Enum):
    """The enum contains the codes of the algorithms."""

    CAESAR = enum.auto()
    VIGENERE = enum.auto()
    AES = enum.auto()


from caesar import Caesar
from vigenere import Vigenere
from aes import AES


def cipher(algorithm):
    """Selects a chiper.

    :param algorithm: algorithm of encryption or decryption
    :type algorithm: int|str

    :return: an object of one of the encryption classes or None
    """

    if isinstance(algorithm, str):
        algorithm = algorithm.upper()
    elif isinstance(algorithm, int):
        for alg in AlgEnum:
            if alg.value == algorithm:
                algorithm = alg.name
    else:
        raise TypeError

    if algorithm == AlgEnum.CAESAR.name:
        return Caesar()
    elif algorithm == AlgEnum.VIGENERE.name:
        return Vigenere()
    elif algorithm == AlgEnum.AES.name:
        return AES()
    return None
