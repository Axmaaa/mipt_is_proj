"""AES ecnryption algorithm."""

import secrets
import Crypto.Cipher.AES as _AES

from ciphers import AlgEnum


class AES():
    """Class contains AES algorithm."""

    def __init__(self):
        # Number of the algorithm
        self.algorithm_number = AlgEnum.AES.value
        # Size of nonce in bytes
        self.nonce_size = 16
        # Size of key in bytes
        self.key_size = 32
        # Size of the data block read to encrypt
        self.data_block_size = _AES.block_size

    def keygen(self):
        """Generates a random key."""

        return secrets.token_bytes(self.key_size + self.nonce_size)


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
        """Encrypts data using AES algorithm in EAX mode.

        :param ifstream: binary input stream
        :type ifstream: BufferedReader

        :param ofstream: binary output stream
        :type ofstream: BufferedWriter

        :param key: concatenation of key and nonce for the algorithm
        :type key: bytes
        """

        nonce = key[self.key_size:]
        aes = _AES.new(key[:self.key_size], _AES.MODE_EAX, nonce=nonce)

        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            if len(data_in) < self.data_block_size:
                data_in = self.pad(data_in)
            data_out = aes.encrypt(data_in)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)


    def decrypt(self, ifstream, ofstream, key, data_size):
        """Decrypts data using AES algorithm in EAX mode.

        :param ifstream: binary input stream
        :type ifstream: BufferedReader

        :param ofstream: binary output stream
        :type ofstream: BufferedWriter

        :param key: concatenation of key and nonce for the algorithm
        :type key: bytes

        :param data_size: size of the payload
        :type data_size: int
        """

        nonce = key[self.key_size:]
        aes = _AES.new(key[:self.key_size], _AES.MODE_EAX, nonce=nonce)

        data_in = ifstream.read(self.data_block_size)
        while data_in != b'':
            if data_size < self.data_block_size:
                data_in = self.unpad(data_in, data_size)
            data_out = aes.decrypt(data_in)
            ofstream.write(data_out)
            data_in = ifstream.read(self.data_block_size)
            data_size -= len(data_in)
