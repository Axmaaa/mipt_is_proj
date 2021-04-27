"""Module for working with header of encrypted file."""

import header_pb2
from hashpw import hashpw
import utils
import ciphers


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


    def add_user(self, symmetric_key, password=None, public_key_file=None):
        """Adds to the header a user who can decrypt the file.

        :param symmetric_key: the key of symmetric-key encryption
        :type: bytes

        :param password: password (in case of symmetric-key encryption)
        :type: str|NoneType

        :param public_key_file: file with public key (in case of hybrid encryption)
        :type public_key_file: str|NoneType
        """

        if utils.is_symmetric(self.algorithm) and password is None:
            raise ValueError('Algorithm is symmetric, but password is None')
        if not utils.is_symmetric(self.algorithm) and public_key_file is None:
            raise ValueError('Algorithm is hybrid, but public key file is None')

        user = self._header.users.add() # pylint: disable=no-member
        if utils.is_symmetric(self.algorithm):
            salt = hashpw.gensalt()
            _hash = hashpw(password, salt)
            passwd_hash = _hash.pw_hash()
            if len(passwd_hash) < len(symmetric_key):
                raise ValueError('Too little hash')
            double_passwd_hash = _hash.double_pw_hash()
            user.salt = salt
            user.uid = double_passwd_hash
            user.enkey = utils.xor_bytes(passwd_hash, symmetric_key)
        else:
            public_cipher = ciphers.public_cipher(self.algorithm)
            public_key = public_cipher.import_key(public_key_file)
            user.uid = public_key.export_key('DER')
            user.enkey = public_cipher.encrypt(public_key, symmetric_key)


    def key(self, password=None, private_key_file=None):
        """Checks if the password matches one of the users.

        :param password: password to check (in case of symmetric-key encryption)
        :type password: str|Nonetype

        :param private_key_file: file with private key (in case of hybrid encryption)
        :type private_key_file: str|NoneType

        :rtype: bytes|NoneType
        :return: the key if the user was found, otherwise None
        """

        if utils.is_symmetric(self.algorithm) and password is None:
            raise ValueError('Algorithm is symmetric, but password is None')
        if not utils.is_symmetric(self.algorithm) and private_key_file is None:
            raise ValueError('Algorithm is hybrid, but private key file is None')

        for user in self._header.users: # pylint: disable=no-member
            if utils.is_symmetric(self.algorithm):
                _hash = hashpw(password, user.salt)
                passwd_hash = _hash.pw_hash()
                if _hash.pw_check(user.uid):
                    return utils.xor_bytes(passwd_hash, user.enkey)
            else:
                public_cipher = ciphers.public_cipher(self.algorithm)
                private_key = public_cipher.import_key(private_key_file)
                if private_key.public_key().export_key('DER') == user.uid:
                    return public_cipher.decrypt(private_key, user.enkey)

        return None


    def __repr__(self):
        return self._header.__repr__()
