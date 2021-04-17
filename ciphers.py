"""Gets a cipher from an algorithm."""

import utils

from caesar import Caesar
from vigenere import Vigenere
from aes import AES
from des import DES
from magma import Magma
from kuznechik import Kuznechik


def cipher(algorithm):
    """Selects a chiper.

    :param algorithm: algorithm of encryption or decryption
    :type algorithm: int|str

    :return: an object of one of the encryption classes or None
    """

    if isinstance(algorithm, str):
        algorithm = algorithm.upper()
    elif isinstance(algorithm, int):
        for alg in utils.AlgEnum:
            if alg.value == algorithm:
                algorithm = alg.name
    else:
        raise TypeError

    __cipher = None
    if algorithm == utils.AlgEnum.CAESAR.name:
        __cipher = Caesar()
    if algorithm == utils.AlgEnum.VIGENERE.name:
        __cipher = Vigenere()
    if algorithm == utils.AlgEnum.AES.name:
        __cipher = AES()
    if algorithm == utils.AlgEnum.DES.name:
        __cipher = DES()
    if algorithm == utils.AlgEnum.MAGMA.name:
        __cipher = Magma()
    if algorithm == utils.AlgEnum.KUZNECHIK.name:
        __cipher = Kuznechik()

    if __cipher is not None:
        return __cipher
    return None
