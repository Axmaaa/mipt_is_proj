"""Caesar ecnryption algorithm."""

import random
from ciphers import AlgEnum


class Caesar():
    """Class contains caesar algorithm."""

    def __init__(self):
        # Number of the algorithm
        self.algorithm_number = AlgEnum.CAESAR.value
        # Size of key in bytes
        self.key_length_bytes = 1
        # Size of key in bits
        self.key_length_bits = self.key_length_bytes * 8
        # Size of the data block read to encrypt
        self.data_block_size = 1024

    def keygen(self):
        """Generates a random key."""

        key = random.getrandbits(self.key_length_bits)
        return key.to_bytes(self.key_length_bytes, byteorder='big')


    def encrypt(self, ifstream, ofstream, key):
        """Encrypts data using caesar algorithm.

        :param ifstream: binary input stream
        :type ifstream: BufferedReader

        :param ofstream: binary output stream
        :type ofstream: BufferedWriter

        :param key: key for the algorithm
        :type key: bytes
        """

        __key = int.from_bytes(key, byteorder='big')
        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            data_out = bytearray()
            for byte in data_in:
                data_out.append((byte + __key) % 256)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)


    def decrypt(self, ifstream, ofstream, key):
        """Decrypts data using caesar algorithm.

        :param ifstream: binary input stream
        :type ifstream: BufferedReader

        :param ofstream: binary output stream
        :type ofstream: BufferedWriter

        :param key: key for the algorithm
        :type key: bytes
        """

        __key = int.from_bytes(key, byteorder='big')
        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            data_out = bytearray()
            for byte in data_in:
                data_out.append((byte - __key) % 256)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)
