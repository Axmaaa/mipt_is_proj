"""Module for working with header of encrypted file."""

import header_pb2
from hashpw import hashpw
from utils import xor_bytes


class Header:
    """Class for storing information from the encrypted file header."""

    def __init__(self):
        self._header = header_pb2.Header()
        # Length of the size of header in bytes
        self.header_size_len = 8
        # Size of the salt in bytes
        self.salt_size = 16


    @property
    def algorithm(self):
        """Encryption algorithm."""

        return self._header.algorithm # pylint: disable=no-member


    @algorithm.setter
    def algorithm(self, algorithm):
        self._header.algorithm = algorithm


    @property
    def data_length(self):
        """The length of the payload."""

        return self._header.data_length # pylint: disable=no-member


    @data_length.setter
    def data_length(self, data_length):
        self._header.data_length = data_length


    def write(self, ofstream):
        """Writes the header to file stream."""

        header_bin = self._header.SerializeToString()
        header_bin_size = len(header_bin)
        ofstream.write(header_bin_size.to_bytes(self.header_size_len, byteorder='little'))
        ofstream.write(header_bin)


    def read(self, ifstream):
        """Reads a header from a file stream."""

        header_size = int.from_bytes(ifstream.read(self.header_size_len), byteorder='little')
        header_bin = ifstream.read(header_size)
        self._header.ParseFromString(header_bin)


    def add_user(self, privkey, passwd=None):
        """Adds to the header a user who can decrypt the file.

        :param passwd: password (in case of symmetric-key encryption)
        :type: str

        :param privkey: the key of symmetric-key encryption
        :type: bytes
        """

        user = self._header.users.add() # pylint: disable=no-member
        if passwd is not None:
            salt = hashpw.gensalt()
            user.salt = salt
            _hash = hashpw(passwd, salt)
            passwd_hash = _hash.pw_hash()
            double_passwd_hash = _hash.double_pw_hash()
            user.uid = double_passwd_hash
            if len(passwd_hash) < len(privkey):
                raise ValueError('Too little hash')
            user.enkey = xor_bytes(passwd_hash, privkey)


    def key(self, passwd=None):
        """Checks if the password matches one of the users.

        :param passwd: password to check
        :type passwd: str

        :rtype: bytes|NoneType
        :return: the key if the user was found, otherwise None
        """

        for user in self._header.users: # pylint: disable=no-member
            if passwd is not None:
                _hash = hashpw(passwd, user.salt)
                passwd_hash = _hash.pw_hash()
                if _hash.pw_check(user.uid):
                    return xor_bytes(passwd_hash, user.enkey)

        return None


    def __repr__(self):
        return self._header.__repr__()
