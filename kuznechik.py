"""GOST 34.12 (aka Kuznechik) ecnryption algorithm."""

import secrets
from Crypto.Util.strxor import strxor
import pygost.gost3412 as gost3412

import utils


class Kuznechik():
    """Class contains Kuznechik algorithm."""

    def __init__(self):
        # Number of the algorithm
        self.algorithm_number = utils.AlgEnum.KUZNECHIK.value
        # Size of initialization vector in bytes
        self.iv_size = gost3412.GOST3412Kuznechik.blocksize
        # Size of key in bytes
        self.key_size = gost3412.KEYSIZE
        # Size of the data block read to encrypt
        self.data_block_size = gost3412.GOST3412Kuznechik.blocksize

    def keygen(self):
        """Generates a random key."""

        return secrets.token_bytes(self.key_size + self.iv_size)


    def encrypt(self, ifstream, ofstream, key):
        """Encrypts data using Magma algorithm in CBC mode.

        :param ifstream: binary input stream
        :type ifstream: BufferedReader

        :param ofstream: binary output stream
        :type ofstream: BufferedWriter

        :param key: key for the algorithm
        :type key: bytes
        """

        kuznechik = gost3412.GOST3412Kuznechik(key[:self.key_size])

        init_vector = key[self.key_size:]
        tmp_data = init_vector

        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            if len(data_in) < self.data_block_size:
                data_in = utils.pad(data_in, self.data_block_size)
            data_in = strxor(data_in, tmp_data)
            data_out = kuznechik.encrypt(data_in)
            tmp_data = data_out
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)


    def decrypt(self, ifstream, ofstream, key, data_size):
        """Decrypts data using Magma algorithm in CBC mode.

        :param ifstream: binary input stream
        :type ifstream: BufferedReader

        :param ofstream: binary output stream
        :type ofstream: BufferedWriter

        :param key: key for the algorithm
        :type key: bytes

        :param data_size: size of the payload
        :type data_size: int
        """

        kuznechik = gost3412.GOST3412Kuznechik(key[:self.key_size])

        init_vector = key[self.key_size:]
        tmp_data = init_vector

        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            data_out = kuznechik.decrypt(data_in)
            data_out = strxor(data_out, tmp_data)
            tmp_data = data_in
            if data_size < self.data_block_size:
                data_out = utils.unpad(data_out, data_size)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)
            data_size -= len(data_in)
