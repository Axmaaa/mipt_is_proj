"""Function hashpw calculates password hash using given hash algorithm."""

import enum
import secrets

import hashlib
from pygost import gost34112012512 as streebog
import bcrypt

PW_SALT_SIZE = 16


class HashEnum(enum.Enum):
    """Class contains the numbers of the hash functions."""

    SHA2256NOSALT = 1
    SHA2256 = enum.auto()
    SHA2512 = enum.auto()
    SHA3512 = enum.auto()
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
            if hash_function.upper() not in [hashf.name for hashf in HashEnum]:
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
    def cls(self):
        """Selects a hash function class.

        :param password: password for hash function
        :type password: bytes

        :param salt: salt for hash function
        :type salt: bytes

        :return: class of one of the hash functions or None
        """

        _hash = None
        if self.hash_function == HashEnum.SHA2256NOSALT.name:
            _hash = SHA2256NoSalt
        if self.hash_function == HashEnum.SHA2256.name:
            _hash = SHA2256
        if self.hash_function == HashEnum.SHA2512.name:
            _hash = SHA2512
        if self.hash_function == HashEnum.SHA3512.name:
            _hash = SHA3512
        if self.hash_function == HashEnum.STREEBOG.name:
            _hash = Streebog
        if self.hash_function == HashEnum.BCRYPT.name:
            _hash = Bcrypt

        return _hash



class HashPw():
    """Contains functions to hash and check passwords."""

    def __init__(self, password, salt=b''):
        self.password = password
        self.salt = salt
        if self.salt == b'':
            self.salt = self.gensalt()


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

        return self.hash() == pw_hash


class SHA2256NoSalt(HashPw):
    """SHA2-256 hash without salt."""

    def hash(self):
        _hash = hashlib.sha256()
        _hash.update(self.password)
        return _hash.digest()


class SHA2256(HashPw):
    """SHA2-256 hash."""

    def hash(self):
        _hash = hashlib.sha256()
        _hash.update(self.password + self.salt)
        return _hash.digest()


class SHA2512(HashPw):
    """SHA2-512 hash."""

    def hash(self):
        _hash = hashlib.sha512()
        _hash.update(self.password + self.salt)
        return _hash.digest()


class SHA3512(HashPw):
    """SHA3-512 hash."""

    def hash(self):
        _hash = hashlib.sha3_512() # pylint: disable=no-member
        _hash.update(self.password + self.salt)
        return _hash.digest()


class Streebog(HashPw):
    """GOST 34.11-2012 (aka Streebog) hash."""

    def hash(self):
        _hash = streebog.new()
        _hash.update(self.password + self.salt)
        return _hash.digest()


class Bcrypt(HashPw):
    """Bcrypt hash."""

    @classmethod
    def gensalt(cls):
        return bcrypt.gensalt()


    def hash(self):
        return bcrypt.hashpw(self.password, self.salt)


    def check(self, pw_hash):
        return bcrypt.checkpw(self.password, pw_hash)


ENC_HASH_FUNCTION = HashFunc('Bcrypt')
