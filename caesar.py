"""Caesar ecnryption algorithm."""

import secrets

import utils


class Caesar():
    """Class contains caesar algorithm."""

    def __init__(self):
        # Number of the algorithm
        self.algorithm_number = utils.AlgEnum.CAESAR.value
        # Size of key in bytes
        self.key_size = 1
        # Size of the data block read to encrypt
        self.data_block_size = 1024

    def keygen(self):
        """Generates a random key."""

        return secrets.token_bytes(self.key_size)


    @staticmethod
    def __encrypt_block(data_block, key):
        """Encrypts data block using caesar algorithm."""

        data_out = bytearray()
        for byte in data_block:
            data_out.append((byte + key) % 256)
        return bytes(data_out)


    @staticmethod
    def __decrypt_block(data_block, key):
        """Decrypts data block using caesar algorithm."""

        data_out = bytearray()
        for byte in data_block:
            data_out.append((byte - key) % 256)
        return bytes(data_out)


    def encrypt(self, ifstream, ofstream, key):
        """Encrypts data using caesar algorithm.

        :param ifstream: binary input stream
        :type ifstream: BufferedReader

        :param ofstream: binary output stream
        :type ofstream: BufferedWriter

        :param key: key for the algorithm
        :type key: bytes, length = 1
        """

        key = ord(key)
        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            data_out = self.__encrypt_block(data_in, key)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)


    def decrypt(self, ifstream, ofstream, key, data_size=None): # pylint: disable=unused-argument
        """Decrypts data using caesar algorithm.

        :param ifstream: binary input stream
        :type ifstream: BufferedReader

        :param ofstream: binary output stream
        :type ofstream: BufferedWriter

        :param key: key for the algorithm
        :type key: bytes, length = 1
        """

        key = ord(key)
        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            data_out = self.__decrypt_block(data_in, key)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)
