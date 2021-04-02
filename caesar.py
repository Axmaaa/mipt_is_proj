"""Caesar ecnryption algorithm."""

import random

# Size of key in bytes
KEY_LENGTH_BYTES = 1
# Size of key in bits
KEY_LENGTH_BITS = KEY_LENGTH_BYTES * 8
# Size of the data block read to encrypt
DATA_BLOCK_SIZE = 1024

def keygen():
    """Generates a random key."""
    return random.getrandbits(KEY_LENGTH_BITS).to_bytes(KEY_LENGTH_BYTES, byteorder='big')


def encrypt(ifstream=None, ofstream=None, key=None):
    """Encrypts data using caesar algorithm."""

    __key = int.from_bytes(key, byteorder='big')
    data_in = ifstream.read(DATA_BLOCK_SIZE)
    while data_in != b'':
        data_out = bytearray()
        for byte in data_in:
            data_out.append((byte + __key) % 256)
        ofstream.write(data_out)
        data_in = ifstream.read(DATA_BLOCK_SIZE)


def decrypt(ifstream=None, ofstream=None, key=None):
    """Decrypts data using caesar algorithm."""

    __key = int.from_bytes(key, byteorder='big')
    data_in = ifstream.read(DATA_BLOCK_SIZE)
    while data_in != b'':
        data_out = bytearray()
        for byte in data_in:
            data_out.append((byte - __key) % 256)
        ofstream.write(data_out)
        data_in = ifstream.read(DATA_BLOCK_SIZE)
