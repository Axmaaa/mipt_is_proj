"""RSA encryption algorithm."""

import Crypto.PublicKey.RSA as _RSA
from Crypto.Cipher import PKCS1_OAEP


class RSA():
    """Class contains RSA algorithm."""

    def __init__(self):
        # Size of key in bytes
        self.key_size = 512
        # Maximum data size in bytes
        self.max_data_size = 214


    def keygen(self):
        """Generates a random key."""

        return _RSA.generate(self.key_size * 8)


    @staticmethod
    def import_key(key_file):
        """Reads key from file."""

        with open(key_file, 'rb') as ifstream:
            key = _RSA.import_key(ifstream.read())
        return key


    @staticmethod
    def encrypt(public_key, data):
        """Encrypts data using RSA PKCS1_OAEP algorithm.

        :param public_key: puclic key for the algorithm
        :type public_key: RSA.RsaKey

        :param data: data to encrypt
        :type data: bytes
        """

        cipher = PKCS1_OAEP.new(public_key)
        return cipher.encrypt(data)


    @staticmethod
    def decrypt(private_key, data):
        """Decrypts data using RSA PKCS1_OAEP algorithm.

        :param private key: key for the algorithm
        :type private key: RSA.RsaKey

        :param data: data to decrypt
        :type data: bytes
        """

        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(data)
