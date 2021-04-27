"""Gets a cipher from an algorithm."""

import utils

from caesar import Caesar
from vigenere import Vigenere
from aes import AES
from des import DES
from magma import Magma
from kuznechik import Kuznechik

from rsa import RSA


def symmetric_cipher(algorithm):
    """Selects a symmetric-key chiper.

    :param algorithm: algorithm of encryption or decryption data
    :type algorithm: int|str

    :return: an object of one of the symmetric-key encryption classes or None
    """

    algorithm = utils.algorithm_name(algorithm)

    _cipher = None
    if algorithm == utils.AlgEnum.CAESAR.name:
        _cipher = Caesar()
    if algorithm == utils.AlgEnum.VIGENERE.name:
        _cipher = Vigenere()
    if algorithm == utils.AlgEnum.AES.name:
        _cipher = AES()
    if algorithm == utils.AlgEnum.DES.name:
        _cipher = DES()
    if algorithm == utils.AlgEnum.MAGMA.name:
        _cipher = Magma()
    if algorithm == utils.AlgEnum.KUZNECHIK.name:
        _cipher = Kuznechik()

    if algorithm == utils.AlgEnum.RSA.name:
        _cipher = Kuznechik()

    return _cipher


def public_cipher(algorithm):
    """Selects a public-key chiper.

    :param algorithm: algorithm of encryption or decryption
    :type algorithm: int|str

    :return: an object of one of the public-key encryption classes or None
    """

    algorithm = utils.algorithm_name(algorithm)

    if utils.is_symmetric(algorithm):
        raise ValueError('Algorithm is symmetric-key')

    _cipher = None
    if algorithm == utils.AlgEnum.RSA.name:
        _cipher = RSA()

    return _cipher
