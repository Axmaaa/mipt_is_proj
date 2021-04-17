"""DES ecnryption algorithm."""

import secrets
import Crypto.Cipher.DES as _DES

import utils


class DES():
    """Class contains DES algorithm."""

    def __init__(self):
        # Number of the algorithm
        self.algorithm_number = utils.AlgEnum.DES.value
        # Mode of the algorithm
        self.mode = _DES.MODE_CBC
        # Size of initializaton vector in bytes
        self.iv_size = 8
        # Size of key in bytes
        self.key_size = _DES.key_size
        # Size of the data block read to encrypt
        self.data_block_size = _DES.block_size

    def keygen(self):
        """Generates a random key."""

        return secrets.token_bytes(self.key_size + self.iv_size)


    def encrypt(self, ifstream, ofstream, key):
        """Encrypts data using DES algorithm in CBC mode.

        :param ifstream: binary input stream
        :type ifstream: BufferedReader

        :param ofstream: binary output stream
        :type ofstream: BufferedWriter

        :param key: concatenation of key and initializaton vector for the algorithm
        :type key: bytes
        """

        init_vector = key[self.key_size:]
        des = _DES.new(key[:self.key_size], self.mode, iv=init_vector)

        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            if len(data_in) < self.data_block_size:
                data_in = utils.pad(data_in, self.data_block_size)
            data_out = des.encrypt(data_in)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)


    def decrypt(self, ifstream, ofstream, key, data_size):
        """Decrypts data using DES algorithm in CBC mode.

        :param ifstream: binary input stream
        :type ifstream: BufferedReader

        :param ofstream: binary output stream
        :type ofstream: BufferedWriter

        :param key: concatenation of key and initializaton vector for the algorithm
        :type key: bytes

        :param data_size: size of the payload
        :type data_size: int
        """

        init_vector = key[self.key_size:]
        des = _DES.new(key[:self.key_size], self.mode, iv=init_vector)

        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            data_out = des.decrypt(data_in)
            if data_size < self.data_block_size:
                data_out = utils.unpad(data_out, data_size)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)
            data_size -= len(data_in)