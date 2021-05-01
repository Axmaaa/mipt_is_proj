"""Vigenere ecnryption algorithm."""

import secrets


class Vigenere():
    """Class contains vigenere algorithm."""

    def __init__(self):
        # Size of key in bytes
        self.key_size = 10
        # Size of key data in bytes
        self.key_data_size = self.key_size
        # Size of the data block read to encrypt
        self.data_block_size = self.key_data_size

    def keygen(self):
        """Generates a random key."""

        return secrets.token_bytes(self.key_data_size)


    @staticmethod
    def __encrypt_block(data_block, key):
        """Encrypts data block using vigenere algorithm."""

        data_out = bytearray()
        for data_byte, key_byte in zip(data_block, key):
            data_out.append((data_byte + key_byte) % 256)
        return bytes(data_out)


    @staticmethod
    def __decrypt_block(data_block, key):
        """Encrypts data block using vigenere algorithm."""

        data_out = bytearray()
        for data_byte, key_byte in zip(data_block, key):
            data_out.append((data_byte - key_byte) % 256)
        return bytes(data_out)


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
            data_out = self.__encrypt_block(data_in, key)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)


    def decrypt(self, ifstream, ofstream, key, data_size=None): # pylint: disable=unused-argument
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
            data_out = self.__decrypt_block(data_in, key)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)
