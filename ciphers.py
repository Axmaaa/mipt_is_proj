"""Gets a cipher from an algorithm."""

import enum


class AlgEnum(enum.Enum):
    """The enum contains the codes of the algorithms."""

    CAESAR = enum.auto()
    VIGENERE = enum.auto()
    AES = enum.auto()
    DES = enum.auto()
    MAGMA = enum.auto()


from caesar import Caesar       # pylint: disable=wrong-import-position
from vigenere import Vigenere   # pylint: disable=wrong-import-position
from aes import AES             # pylint: disable=wrong-import-position
from des import DES             # pylint: disable=wrong-import-position
from magma import Magma         # pylint: disable=wrong-import-position


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
    if algorithm == AlgEnum.VIGENERE.name:
        return Vigenere()
    if algorithm == AlgEnum.AES.name:
        return AES()
    if algorithm == AlgEnum.DES.name:
        return DES()
    if algorithm == AlgEnum.MAGMA.name:
        return Magma()
    return None
