"""Module for generating key from password."""

import secrets
from hashlib import scrypt


KEY_SALT_SIZE = 16


def gensalt():
    """Generates random salt for password."""

    return secrets.token_bytes(KEY_SALT_SIZE)



def kdf(password, key_salt, key_size):
    """Generates key based on password and salt."""

    return scrypt(password, salt=key_salt, n=2**14, r=8, p=1, dklen=key_size)
    # return pbkdf2_hmac('sha256', password, key_salt, 100000, dklen=key_size)