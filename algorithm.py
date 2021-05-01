"""Module contains algorithm class."""

import enum

from caesar import Caesar
from vigenere import Vigenere
from aes import AES
from des import DES
from magma import Magma
from kuznechik import Kuznechik

from rsa import RSA


class AlgEnum(enum.Enum):
    """The enum contains the codes of the algorithms."""

    CAESAR = 1
    VIGENERE = enum.auto()
    AES = enum.auto()
    DES = enum.auto()
    MAGMA = enum.auto()
    KUZNECHIK = enum.auto()

    RSA = enum.auto()


class Algorithm():
    """Class contains algorithm data."""

    def __init__(self, algorithm):
        """
        :param algorithm: algorithm
        :type algorithm: int|str
        """
        if isinstance(algorithm, str):
            if algorithm.upper() not in [alg.name for alg in AlgEnum]:
                raise ValueError('Invalid algorithm name')
            self.algorithm = algorithm.upper()
        elif isinstance(algorithm, int):
            if algorithm not in [alg.value for alg in AlgEnum]:
                raise ValueError('Invalid algorithm number')
            self.algorithm = AlgEnum(algorithm).name
        else:
            raise TypeError('Invalid alorithm type')
        self.key_data_size = self.symmetric_cipher().key_data_size


    @property
    def name(self):
        """Returns the name of the algorithm."""

        return self.algorithm


    @property
    def number(self):
        """Returns the number of the algorithm."""

        return AlgEnum[self.algorithm].value


    def is_symmetric(self):
        """True if the encryption algorithm is symmetric."""

        return self.number < AlgEnum.RSA.value # The first public-key algorithm in enum


    def symmetric_cipher(self):
        """Selects a symmetric-key chiper.

        :return: an object of one of the symmetric-key encryption classes or None
        """

        _cipher = None
        if self.algorithm == AlgEnum.CAESAR.name:
            _cipher = Caesar()
        if self.algorithm == AlgEnum.VIGENERE.name:
            _cipher = Vigenere()
        if self.algorithm == AlgEnum.AES.name:
            _cipher = AES()
        if self.algorithm == AlgEnum.DES.name:
            _cipher = DES()
        if self.algorithm == AlgEnum.MAGMA.name:
            _cipher = Magma()
        if self.algorithm == AlgEnum.KUZNECHIK.name:
            _cipher = Kuznechik()

        if self.algorithm == AlgEnum.RSA.name:
            _cipher = Kuznechik()

        return _cipher


    def public_cipher(self):
        """Selects a public-key chiper.

        :return: an object of one of the public-key encryption classes or None
        """

        if self.is_symmetric():
            raise ValueError('Algorithm is symmetric-key')

        _cipher = None
        if self.algorithm == AlgEnum.RSA.name:
            _cipher = RSA()

        return _cipher
