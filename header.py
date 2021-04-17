"""Module for working with header of encrypted file."""

import secrets

import header_pb2
import hash_func
from utils import xor_bytes

# Length of the size of header in bytes
HEADER_SIZE_LEN = 8
# Size of the salt in bytes
SALT_LEN_BYTES = 16

class Header:
    """Class for storing information from the encrypted file header."""

    def __init__(self):
        self.__header = header_pb2.Header()


    @property
    def algorithm(self):
        """Encryption algorithm."""

        return self.__header.algorithm # pylint: disable=no-member


    @algorithm.setter
    def algorithm(self, algorithm):
        self.__header.algorithm = algorithm


    @property
    def data_length(self):
        """The length of the payload."""

        return self.__header.data_length # pylint: disable=no-member


    @data_length.setter
    def data_length(self, data_length):
        self.__header.data_length = data_length


    def write(self, ofstream):
        """Writes the header to file stream."""

        header_bin = self.__header.SerializeToString()
        header_bin_size = len(header_bin)
        ofstream.write(header_bin_size.to_bytes(HEADER_SIZE_LEN, byteorder='little'))
        ofstream.write(header_bin)


    def read(self, ifstream):
        """Reads a header from a file stream."""

        header_bin_size = int.from_bytes(ifstream.read(HEADER_SIZE_LEN), byteorder='little')
        header_bin = ifstream.read(header_bin_size)
        self.__header.ParseFromString(header_bin)


    def add_user(self, privkey, passwd=None):
        """Adds to the header a user who can decrypt the file.

        :param passwd: password (in case of symmetric-key encryption)
        :type: str

        :param privkey: the key of symmetric-key encryption
        :type: bytes
        """

        user = self.__header.users.add() # pylint: disable=no-member
        if passwd is not None:
            salt = secrets.token_bytes(SALT_LEN_BYTES)
            user.salt = salt
            salty_passwd = bytes(passwd, encoding='ascii') + salt
            passwd_hash = hash_func.hash_func(salty_passwd)
            double_passwd_hash = hash_func.hash_func(passwd_hash)
            user.uid = double_passwd_hash
            if len(double_passwd_hash) < len(privkey):
                raise ValueError('Too little hash')
            user.enkey = xor_bytes(double_passwd_hash, privkey)


    def key(self, passwd=None):
        """Checks if the password matches one of the users.

        :param passwd: password to check
        :type passwd: str

        :rtype: bytes|NoneType
        :return: the key if the user was found, otherwise None
        """

        for user in self.__header.users: # pylint: disable=no-member
            if passwd is not None:
                salty_passwd = bytes(passwd, encoding='ascii') + user.salt
                passwd_hash = hash_func.hash_func(salty_passwd)
                double_passwd_hash = hash_func.hash_func(passwd_hash)
                if double_passwd_hash == user.uid:
                    return xor_bytes(user.uid, user.enkey)

        return None


    def __repr__(self):
        return self.__header.__repr__()
