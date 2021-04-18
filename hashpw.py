"""Function hash_func calculates a hash using given hash algorithm."""

import secrets

from hashlib import sha512
from pygost import gost34112012512 as streebog
import bcrypt

SALT_SIZE = 16


class HashPw():
    """Contains functions to hash passwords."""

    def __init__(self, passwd, salt):
        self.password = bytes(passwd, encoding='ascii')
        self.salt = salt


    @classmethod
    def gensalt(cls):
        """Generates random salt."""

        salt = secrets.token_bytes(SALT_SIZE)
        return salt


    def pw_hash(self):
        """Returns hash of salty password."""

        pass


    def double_pw_hash(self):
        """Returns hash of hash of salty password."""

        pass


    def pw_check(self, double_password_hash):
        """Checks if hash(hash(salty_passwd)) equals to double_password_hash."""

        return self.double_pw_hash() == double_password_hash


class SHA512(HashPw):
    """SHA-512 hash."""

    def pw_hash(self):
        _hash = sha512()
        _hash.update(self.password + self.salt)
        return _hash.digest()


    def double_pw_hash(self):
        _hash = sha512()
        _hash.update(self.pw_hash())
        return _hash.digest()


class Streebog(HashPw):
    """GOST 34.11-2012 (aka Streebog) hash."""

    def pw_hash(self):
        _hash = streebog.new()
        _hash.update(self.password + self.salt)
        return _hash.digest()


    def double_pw_hash(self):
        _hash = streebog.new()
        _hash.update(self.pw_hash())
        return _hash.digest()


class Bcrypt(HashPw):
    """Bcrypt hash."""

    @classmethod
    def gensalt(cls):
        return bcrypt.gensalt()


    def pw_hash(self):
        return bcrypt.hashpw(self.password, self.salt)


    def double_pw_hash(self):
        return bcrypt.hashpw(self.pw_hash(), self.salt)

hashpw = Streebog # pylint: disable=invalid-name
