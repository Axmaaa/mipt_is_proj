"""AES ecnryption algorithm."""

import secrets
import Crypto.Cipher.AES as _AES

import utils


class AES():
    """Class contains AES algorithm."""

    def __init__(self):
        # Number of the algorithm
        self.algorithm_number = utils.AlgEnum.AES.value
        # Mode of the algorithm
        self.mode = _AES.MODE_CBC
        # Size of initializaton vector in bytes
        self.iv_size = 16
        # Size of key in bytes
        self.key_size = _AES.key_size[2]
        # Size of the data block read to encrypt
        self.data_block_size = _AES.block_size

    def keygen(self):
        """Generates a random key."""

        return secrets.token_bytes(self.key_size + self.iv_size)


    def encrypt(self, ifstream, ofstream, key):
        """Encrypts data using AES algorithm in CBC mode.

        :param ifstream: binary input stream
        :type ifstream: BufferedReader

        :param ofstream: binary output stream
        :type ofstream: BufferedWriter

        :param key: concatenation of key and initializaton vector for the algorithm
        :type key: bytes
        """

        init_vector = key[self.key_size:]
        aes = _AES.new(key[:self.key_size], self.mode, iv=init_vector)

        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            if len(data_in) < self.data_block_size:
                data_in = utils.pad(data_in, self.data_block_size)
            data_out = aes.encrypt(data_in)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)


    def decrypt(self, ifstream, ofstream, key, data_size):
        """Decrypts data using AES algorithm in CBC mode.

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
        aes = _AES.new(key[:self.key_size], self.mode, iv=init_vector)

        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            data_out = aes.decrypt(data_in)
            if data_size < self.data_block_size:
                data_out = utils.unpad(data_out, data_size)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)
            data_size -= len(data_in)
