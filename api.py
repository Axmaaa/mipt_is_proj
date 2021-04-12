"""API for encryption and decryption files."""

import os.path

import header
import ciphers


def encrypt_file(input_file, output_file, algorithm, passwords):
    """Encrypts input file.

    :param input_file: file with plain text
    :type input_file: str

    :param output_file: file for encryptes text
    :type output_file: str

    :param algorithm: algorithm used to encrypt
    :type algorithm: str

    :param passwords: list of passwords to decrypt the file
    :type passwords: list

    """

    cipher = ciphers.cipher(algorithm)

    hdr = header.Header()
    hdr.algorithm = cipher.algorithm_number
    hdr.data_length = os.path.getsize(input_file)

    key = cipher.keygen()
    for password in passwords:
        hdr.add_user(key, password)

    with open(input_file, 'rb') as ifstream:
        with open(output_file, 'wb') as ofstream:
            hdr.write(ofstream)
            cipher.encrypt(ifstream, ofstream, key)


def decrypt_file(input_file, output_file, password):
    """Decrypts input file."""

    hdr = header.Header()
    with open(input_file, 'rb') as ifstream:
        hdr.read(ifstream)
        algorithm = hdr.algorithm
        cipher = ciphers.cipher(algorithm)
        data_length = hdr.data_length

        key = hdr.key(password)
        if key is None:
            raise ValueError
        else:
            with open(output_file, 'wb') as ofstream:
                cipher.decrypt(ifstream, ofstream, key, data_length)
