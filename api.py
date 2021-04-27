"""API for encryption and decryption files."""

import os.path

import utils
import header
import ciphers


def encrypt_file(input_file, output_file, algorithm, passwords=None, public_key_files=None):
    """Encrypts input file.

    :param input_file: file with plain text
    :type input_file: str

    :param output_file: file for encryptes text
    :type output_file: str

    :param algorithm: algorithm used to encrypt
    :type algorithm: str

    :param passwords: list of passwords to decrypt the file
    :type passwords: list

    :param public_key_files: list of files with public keys to encrypt the symmetric key
    :type public_key_files: list
    """

    if utils.is_symmetric(algorithm) and passwords is None:
        raise ValueError('Algorithm is symmetric, but passwords are None')
    if not utils.is_symmetric(algorithm) and public_key_files is None:
        raise ValueError('Algorithm is hybrid, but public key files are None')

    hdr = header.Header()
    hdr.algorithm = utils.algorithm_number(algorithm)
    hdr.data_length = os.path.getsize(input_file)

    symmetric_cipher = ciphers.symmetric_cipher(algorithm)
    symmetric_key = symmetric_cipher.keygen()
    if utils.is_symmetric(algorithm):
        for password in passwords:
            hdr.add_user(symmetric_key, password=password)
    else:
        for public_key_file in public_key_files:
            hdr.add_user(symmetric_key, public_key_file=public_key_file)

    with open(input_file, 'rb') as ifstream:
        with open(output_file, 'wb') as ofstream:
            hdr.write(ofstream)
            symmetric_cipher.encrypt(ifstream, ofstream, symmetric_key)


def decrypt_file(input_file, output_file, password=None, private_key_file=None):
    """Decrypts input file."""

    hdr = header.Header()
    with open(input_file, 'rb') as ifstream:
        hdr.read(ifstream)
        algorithm = hdr.algorithm
        symmetric_cipher = ciphers.symmetric_cipher(algorithm)
        data_length = hdr.data_length

        if utils.is_symmetric(algorithm) and password is None:
            raise ValueError('Algorithm is symmetric, but password is None')
        if not utils.is_symmetric(algorithm) and private_key_file is None:
            raise ValueError('Algorithm is hybrid, but private key file is None')

        if utils.is_symmetric(algorithm):
            symmetric_key = hdr.key(password=password)
            if symmetric_key is None:
                raise ValueError('Invalid password')
        else:
            symmetric_key = hdr.key(private_key_file=private_key_file)
            if symmetric_key is None:
                raise ValueError('Invalid private key')

        with open(output_file, 'wb') as ofstream:
            symmetric_cipher.decrypt(ifstream, ofstream, symmetric_key, data_length)
