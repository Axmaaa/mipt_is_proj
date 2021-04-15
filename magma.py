"""GOST 28147-89 (aka Magma) ecnryption algorithm."""

import secrets
import pygost.gost28147 as magma

from ciphers import AlgEnum


class Magma():
    """Class contains Magma algorithm."""

    def __init__(self):
        # Number of the algorithm
        self.algorithm_number = AlgEnum.MAGMA.value
        # Size of initialization vector
        self.iv_size = magma.BLOCKSIZE
        # Size of key in bytes
        self.key_size = magma.KEYSIZE
        # Size of the data block read to encrypt
        self.data_block_size = magma.BLOCKSIZE

    def keygen(self):
        """Generates a random key."""

        return secrets.token_bytes(self.key_size + self.iv_size)


    def pad(self, data):
        """Pads data with random bytes."""

        if len(data) < self.data_block_size:
            padding_size = self.data_block_size - len(data)
            padding = secrets.token_bytes(padding_size)
        return data + padding


    def unpad(self, data, size):
        """Unpads data."""

        if len(data) != self.data_block_size:
            raise ValueError('Invalid data length')
        return data[:size]


    def encrypt(self, ifstream, ofstream, key):
        """Encrypts data using Magma algorithm in CFB mode.

        :param ifstream: binary input stream
        :type ifstream: BufferedReader

        :param ofstream: binary output stream
        :type ofstream: BufferedWriter

        :param key: key for the algorithm
        :type key: bytes
        """

        init_vector = key[self.key_size:]

        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            if len(data_in) < self.data_block_size:
                data_in = self.pad(data_in)
            data_out = magma.cfb_encrypt(key[:self.key_size], data_in, iv=init_vector)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)


    def decrypt(self, ifstream, ofstream, key, data_size):
        """Decrypts data using Magma algorithm in CFB mode.

        :param ifstream: binary input stream
        :type ifstream: BufferedReader

        :param ofstream: binary output stream
        :type ofstream: BufferedWriter

        :param key: key for the algorithm
        :type key: bytes

        :param data_size: size of the payload
        :type data_size: int
        """

        init_vector = key[self.key_size:]

        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            if data_size < self.data_block_size:
                data_in = self.unpad(data_in, data_size)
            data_out = magma.cfb_decrypt(key[:self.key_size], data_in, iv=init_vector)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)
            data_size -= len(data_in)
