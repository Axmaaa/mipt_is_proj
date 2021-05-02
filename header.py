"""Module for working with header of encrypted file."""

import header_pb2
import hashpw
import kdf
import utils
from algorithm import Algorithm


class Header:
    """Class for storing information from the encrypted file header."""

    def __init__(self):
        self._header = header_pb2.Header()
        # Length of the size of header in bytes
        self.header_size_len = 8


    @property
    def algorithm(self):
        """Encryption algorithm."""

        return self._header.algorithm # pylint: disable=no-member


    @algorithm.setter
    def algorithm(self, algorithm):
        self._header.algorithm = algorithm


    @property
    def hash_function(self):
        """Function to hash password."""

        return self._header.hash_function # pylint: disable=no-member


    @hash_function.setter
    def hash_function(self, hash_function):
        self._header.hash_function = hash_function


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


    def add_user(self, symmkey, password=None, pubkey_file=None):
        """Adds to the header a user who can decrypt the file.

        :param symmkey: key for symmetric key algorithm
        :type symmkey: bytes

        :param password: password (in case of symmetric-key encryption)
        :type: bytes|NoneType

        :param pubkey_file: file with public key (in case of hybrid encryption)
        :type pubkey_file: str|NoneType
        """

        algorithm = Algorithm(self.algorithm)

        if algorithm.is_symmetric() and password is None:
            raise ValueError('Algorithm is symmetric, but password is None')
        if not algorithm.is_symmetric() and pubkey_file is None:
            raise ValueError('Algorithm is hybrid, but public key file is None')

        user = self._header.users.add() # pylint: disable=no-member
        if algorithm.is_symmetric():
            user.key_salt = kdf.gensalt()
            key_pw_hash = kdf.kdf(password, user.key_salt, algorithm.key_data_size)

            hashf_cls = hashpw.HashFunc(self.hash_function).cls
            _hash = hashf_cls(password)
            user.pw_salt = _hash.salt
            user.uid = _hash.hash()

            user.enkey = utils.xor_bytes(key_pw_hash, symmkey)
        else:
            public_cipher = algorithm.public_cipher()
            public_key = public_cipher.import_key(pubkey_file)
            padded_symmkey = utils.pad(symmkey, public_cipher.max_data_size)

            user.uid = public_key.export_key('DER')
            user.enkey = public_cipher.encrypt(public_key, padded_symmkey)


    def key(self, password=None, privkey_file=None):
        """Checks if the password matches one of the users.

        :param password: password to check (in case of symmetric-key encryption)
        :type password: str|Nonetype

        :param privkey_file: file with private key (in case of hybrid encryption)
        :type privkey_file: str|NoneType

        :rtype: bytes|NoneType
        :return: the key if the user was found, otherwise None
        """

        algorithm = Algorithm(self.algorithm)

        if algorithm.is_symmetric() and password is None:
            raise ValueError('Algorithm is symmetric, but password is None')
        if not algorithm.is_symmetric() and privkey_file is None:
            raise ValueError('Algorithm is hybrid, but private key file is None')

        for user in self._header.users: # pylint: disable=no-member
            if algorithm.is_symmetric():
                hashf_cls = hashpw.HashFunc(self.hash_function).cls
                _hash = hashf_cls(password, user.pw_salt)
                if _hash.check(user.uid):
                    key_pw_hash = kdf.kdf(password, user.key_salt, algorithm.key_data_size)
                    return utils.xor_bytes(user.enkey, key_pw_hash)
            else:
                public_cipher = algorithm.public_cipher()
                private_key = public_cipher.import_key(privkey_file)
                if private_key.public_key().export_key('DER') == user.uid:
                    padded_symmkey = public_cipher.decrypt(private_key, user.enkey)
                    return utils.unpad(padded_symmkey, algorithm.key_data_size)

        return None


    def __repr__(self):
        return self._header.__repr__()
