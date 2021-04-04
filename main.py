#!/usr/bin/python3

"""Main."""

import header
import ciphers


def encrypt_file(input_file, output_file, algorithm, passwords):
    """Encrypts input file.

    :param input_file: file with plain text
    :type input_file: BufferedReader

    :param output_file: file for encryptes text
    :type output_file: BufferedWriter

    :param algorithm: algorithm used to encrypt
    :type algorithm: str

    :param passwords: list of passwords to decrypt the file
    :type passwords: list

    """

    cipher = ciphers.cipher(algorithm)
    hdr = header.Header()
    hdr.algorithm = cipher.algorithm_number
    hdr.users_count = len(passwords)
    key = cipher.keygen()
    for password in passwords:
        hdr.add_user(False, password, key)

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
        key = hdr.key(password)
        if key is None:
            raise ValueError
        else:
            with open(output_file, 'wb') as ofstream:
                cipher.decrypt(ifstream, ofstream, key)


passwords = [
    'qwerty123',
    'payalnik',
    'slozhnyy_parol'
    ]

input_file = 'file.in'
enc_file = 'file.enc'
dec_file = 'file.dec'

encrypt_file(input_file, enc_file, 'caesar', passwords)
print('File was encrypted')

passwd = input('Input password: ')
try:
    decrypt_file(enc_file, dec_file, passwd)
except ValueError:
    print('Invalid password!')
else:
    print('File was decrypted')
