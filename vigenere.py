"""Vigenere ecnryption algorithm."""

import random
from ciphers import AlgEnum


class Vigenere():
    """Class contains vigenere algorithm."""

    def __init__(self):
        # Number of the algorithm
        self.algorithm_number = AlgEnum.VIGENERE.value
        # Size of key in bytes
        self.key_length_bytes = 10
        # Size of key in bits
        self.key_length_bits = self.key_length_bytes * 8
        # Size of the data block read to encrypt
        self.data_block_size = self.key_length_bytes

    def keygen(self):
        """Generates a random key."""

        key = random.getrandbits(self.key_length_bits)
        return key.to_bytes(self.key_length_bytes, byteorder='big')


    def encrypt(self, ifstream, ofstream, key):
        """Encrypts data using vigenere algorithm.

        :param ifstream: binary input stream
        :type ifstream: BufferedReader

        :param ofstream: binary output stream
        :type ofstream: BufferedWriter

        :param key: key for the algorithm
        :type key: bytes
        """

        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            data_out = bytearray()
            for data_byte, key_byte in zip(data_in, key):
                data_out.append((data_byte + key_byte) % 256)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)


    def decrypt(self, ifstream, ofstream, key):
        """Decrypts data using vigenere algorithm.

        :param ifstream: binary input stream
        :type ifstream: BufferedReader

        :param ofstream: binary output stream
        :type ofstream: BufferedWriter

        :param key: key for the algorithm
        :type key: bytes
        """

        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            data_out = bytearray()
            for data_byte, key_byte in zip(data_in, key):
                data_out.append((data_byte - key_byte) % 256)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)