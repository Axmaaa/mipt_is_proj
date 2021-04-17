"""Module contains some useful things."""

import enum
import secrets


class AlgEnum(enum.Enum):
    """The enum contains the codes of the algorithms."""

    CAESAR = enum.auto()
    VIGENERE = enum.auto()
    AES = enum.auto()
    DES = enum.auto()
    MAGMA = enum.auto()
    KUZNECHIK = enum.auto()


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
