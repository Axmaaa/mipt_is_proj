"""Function hash_func calculates a hash using given hash algorithm."""

import hashlib

def hash_func(bstr):
    """Calculates a hash."""

    __hash = hashlib.sha256()
    __hash.update(bstr)
    return __hash.digest()
