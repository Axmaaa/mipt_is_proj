"""API for encryption and decryption files."""

import os.path

import header
from algorithm import Algorithm
import hashpw


def encrypt_file(input_file, output_file, algorithm, passwords=None, pubkey_files=None):
    """Encrypts input file.

    :param input_file: file with plain text
    :type input_file: str

    :param output_file: file for encryptes text
    :type output_file: str

    :param algorithm: algorithm used to encrypt
    :type algorithm: str

    :param passwords: list of passwords to decrypt the file
    :type passwords: list

    :param pubkey_files: list of files with public keys to encrypt the symmetric key
    :type pubkey_files: list
    """

    algorithm = Algorithm(algorithm)

    if algorithm.is_symmetric() and passwords is None:
        raise ValueError('Algorithm is symmetric, but passwords are None')
    if not algorithm.is_symmetric() and pubkey_files is None:
        raise ValueError('Algorithm is hybrid, but public key files are None')

    hdr = header.Header()
    hdr.algorithm = algorithm.number
    hashf = hashpw.enc_hash()
    hdr.hash_function = hashf.number
    hdr.data_length = os.path.getsize(input_file)

    symm_cipher = algorithm.symmetric_cipher()
    symmkey = symm_cipher.keygen()
    if algorithm.is_symmetric():
        for password in passwords:
            password = password.encode()
            hdr.add_user(symmkey, password=password)
    else:
        for pubkey_file in pubkey_files:
            hdr.add_user(symmkey, pubkey_file=pubkey_file)

    with open(input_file, 'rb') as ifstream:
        with open(output_file, 'wb') as ofstream:
            hdr.write(ofstream)
            symm_cipher.encrypt(ifstream, ofstream, symmkey)


def decrypt_file(input_file, output_file, password=None, privkey_file=None):
    """Decrypts input file."""

    hdr = header.Header()
    with open(input_file, 'rb') as ifstream:
        hdr.read(ifstream)
        algorithm = Algorithm(hdr.algorithm)
        data_length = hdr.data_length
        symm_cipher = algorithm.symmetric_cipher()

        if algorithm.is_symmetric() and password is None:
            raise ValueError('Algorithm is symmetric, but password is None')
        if not algorithm.is_symmetric() and privkey_file is None:
            raise ValueError('Algorithm is hybrid, but private key file is None')

        if algorithm.is_symmetric():
            password = password.encode()
            symmkey = hdr.key(password=password)
            if symmkey is None:
                raise ValueError('Invalid password')
        else:
            symmkey = hdr.key(privkey_file=privkey_file)
            if symmkey is None:
                raise ValueError('Invalid private key')

        with open(output_file, 'wb') as ofstream:
            symm_cipher.decrypt(ifstream, ofstream, symmkey, data_length)
