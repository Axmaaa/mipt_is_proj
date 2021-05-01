"""Function hashpw calculates password hash using given hash algorithm."""

import enum
import secrets

from hashlib import sha512
from pygost import gost34112012512 as streebog
import bcrypt

PW_SALT_SIZE = 16


class HashEnum(enum.Enum):
    """Class contains the numbers of the hash functions."""

    SHA512 = 1
    STREEBOG = enum.auto()
    BCRYPT = enum.auto()


class HashFunc():
    """Class contains hash function data."""

    def __init__(self, hash_function):
        """
        :param hash_function: hash function
        :type hash_function: int|str
        """
        if isinstance(hash_function, str):
            hash_function = hash_function.upper()
            if hash_function not in [hashf.name for hashf in HashEnum]:
                raise ValueError('Invalid hash function name')
            self.hash_function = hash_function
        elif isinstance(hash_function, int):
            if hash_function not in [hashf.value for hashf in HashEnum]:
                raise ValueError('Invalid hash function number')
            self.hash_function = HashEnum(hash_function).name
        else:
            raise TypeError('Invalid hash function type')


    @property
    def name(self):
        """Returns the name of the hash function."""

        return self.hash_function


    @property
    def number(self):
        """Returns the number of the hash function."""

        return HashEnum[self.hash_function].value


    @property
    def hpw_class(self):
        """Selects a hash function class.

        :param password: password for hash function
        :type password: bytes

        :param salt: salt for hash function
        :type salt: bytes

        :return: class of one of the hash functions or None
        """

        _hash = None
        if self.hash_function == HashEnum.SHA512.name:
            _hash = SHA512
        if self.hash_function == HashEnum.STREEBOG.name:
            _hash = Streebog
        if self.hash_function == HashEnum.BCRYPT.name:
            _hash = Bcrypt

        return _hash



class HashPw():
    """Contains functions to hash and check passwords."""

    def __init__(self, password, salt=b''):
        self.password = password
        if salt == b'':
            self.salt = self.gensalt()
        else:
            self.salt = salt


    @classmethod
    def gensalt(cls):
        """Generates random salt."""

        salt = secrets.token_bytes(PW_SALT_SIZE)
        return salt


    def hash(self):
        """Returns hash of salty password."""

        pass


    def check(self, pw_hash):
        """Checks if hash(salty_passwd) equals to pw_hash."""

        pass


class SHA512(HashPw):
    """SHA-512 hash."""

    def hash(self):
        _hash = sha512()
        _hash.update(self.password + self.salt)
        return _hash.digest()


    def check(self, pw_hash):
        return self.hash() == pw_hash


class Streebog(HashPw):
    """GOST 34.11-2012 (aka Streebog) hash."""

    def hash(self):
        _hash = streebog.new()
        _hash.update(self.password + self.salt)
        return _hash.digest()


    def check(self, pw_hash):
        return self.hash() == pw_hash


class Bcrypt(HashPw):
    """Bcrypt hash."""

    @classmethod
    def gensalt(cls):
        return bcrypt.gensalt()


    def hash(self):
        return bcrypt.hashpw(self.password, self.salt)


    def check(self, pw_hash):
        return bcrypt.checkpw(self.password, pw_hash)


def enc_hash():
    """Returns class of last implemented hash function."""

    for _hash in HashEnum:
        hashf = HashFunc(_hash.name)

    return hashf
