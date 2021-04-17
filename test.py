#!/usr/bin/python3

"""Test the application."""

import os
import secrets
import string

import api


def test(algorithm):
    """Tests correctness of the algorithm.

    :param algorithm: algorithm for test
    :type algorithm: str
    """

    plain_file = 'file_' + algorithm + '.in'
    enc_file = 'file_' + algorithm + '.enc'
    dec_file = 'file_' + algorithm + '.dec'

    min_text_size = 100
    text_size_range = 500
    data_size = min_text_size + secrets.randbelow(text_size_range)
    data = secrets.token_bytes(data_size)
    with open(plain_file, 'wb') as ofstream:
        ofstream.write(data)

    passwords_count = 3
    password_alphabet = string.ascii_letters + string.digits
    passwords = list()
    min_passwd_size = 10
    passwd_size_range = 20
    for _ in range(passwords_count):
        passwd_size = min_passwd_size + secrets.randbelow(passwd_size_range)
        passwd = ''.join(secrets.choice(password_alphabet) for _ in range(passwd_size))
        passwords.append(passwd)

    api.encrypt_file(plain_file, enc_file, algorithm, passwords)

    for passwd in passwords:
        try:
            api.decrypt_file(enc_file, dec_file, passwd)
        except ValueError:
            print('{}: Password {} is invalid!'.format(algorithm, passwd))
            return False
        else:
            with open(dec_file, 'rb') as ifstream:
                dec_data = ifstream.read()
                if dec_data != data:
                    print('{}: Plain text is not equal to decryptes data!'.format(algorithm))
                    print('{}: Plain text:     {}'.format(algorithm, data))
                    print('{}: Decrypted data: {}'.format(algorithm, dec_data))
                    return False
    os.remove(plain_file)
    os.remove(enc_file)
    os.remove(dec_file)
    return True

def main():
    """Main."""

    algorithms = ['caesar', 'vigenere', 'aes', 'des', 'magma', 'kuznechik']
    for alg in algorithms:
        if not test(alg):
            print('\033[31m{} has not passed the test\033[0m'.format(alg))
        else:
            print('\033[32m{} has passed the test\033[0m'.format(alg))

main()
