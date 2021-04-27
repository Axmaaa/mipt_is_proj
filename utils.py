"""Module contains some useful things."""

import enum
import secrets


class AlgEnum(enum.Enum):
    """The enum contains the codes of the algorithms."""

    CAESAR = 1
    VIGENERE = enum.auto()
    AES = enum.auto()
    DES = enum.auto()
    MAGMA = enum.auto()
    KUZNECHIK = enum.auto()

    RSA = enum.auto()


def validate_algorithm(algorithm):
    """Checks if the algorithm exists.

    :param algorithm: algorithm
    :type algorithm: int|str
    """

    if isinstance(algorithm, str):
        if algorithm.upper() not in [alg.name for alg in AlgEnum]:
            raise ValueError('Invalid algorithm name')
    elif isinstance(algorithm, int):
        if algorithm not in [alg.value for alg in AlgEnum]:
            raise ValueError('Invalid algorithm number')
    else:
        raise TypeError('Invalid alorithm type')


def algorithm_name(algorithm):
    """Returns the name of the algorithm.

    :param algorithm: algorithm to get the name of
    :type algorithm: int|str

    :rtype: str
    :return: the name of the algorithm
    """

    validate_algorithm(algorithm)

    if isinstance(algorithm, str):
        return algorithm.upper()
    return AlgEnum(algorithm).name


def algorithm_number(algorithm):
    """Returns the number of the algorithm.

    :param algorithm: algorithm to get the number of
    :type algorithm: int|str

    :rtype: int|None
    :return: the number of the algorithm
    """

    validate_algorithm(algorithm)

    if isinstance(algorithm, str):
        for alg in AlgEnum:
            if alg.name == algorithm.upper():
                return alg.value
    return algorithm


def is_symmetric(algorithm):
    """True if the encryption algorithm is symmetric."""

    validate_algorithm(algorithm)

    algorithm = algorithm_number(algorithm)

    return algorithm < AlgEnum.RSA.value # The first public-key algorithm


def pad(data, padded_data_size):
    """Pads data with random bytes."""

    if len(data) < padded_data_size:
        padding_size = padded_data_size - len(data)
        padding = secrets.token_bytes(padding_size)
    return data + padding


def unpad(data, size):
    """Unpads data."""

    return data[:size]


def xor_bytes(bstr1, bstr2):
    """Returns xor of two byte strings."""

    return bytes([_a ^ _b for _a, _b in zip(bstr1, bstr2)])
