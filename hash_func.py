"""Function hash_func calculates a hash using given hash algorithm."""

import hashlib

def hash_func(data):
    """Calculates a hash."""

    __hash = hashlib.sha512()
    __hash.update(data)
    return __hash.digest()
