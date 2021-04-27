#!/usr/bin/python3

"""Test the application."""

import os
import secrets
import string

import utils
import ciphers
import api


def test(algorithm):
    """Tests correctness of the algorithm.

    :param algorithm: algorithm for test
    :type algorithm: str
    """

    plain_file = 'file_' + algorithm + '.in'
    enc_file = 'file_' + algorithm + '.enc'
    dec_file = 'file_' + algorithm + '.dec'

    data_size = 100 + secrets.randbelow(400)
    data = secrets.token_bytes(data_size)
    with open(plain_file, 'wb') as ofstream:
        ofstream.write(data)

    if utils.is_symmetric(algorithm):
        public_key_files = None
        passwords_count = 3
        password_alphabet = string.ascii_letters + string.digits
        passwords = list()
        for _ in range(passwords_count):
            passwd_size = 10 + secrets.randbelow(20)
            passwd = ''.join(secrets.choice(password_alphabet) for _ in range(passwd_size))
            passwords.append(passwd)
    else:
        passwords = None
        public_key_count = 3
        private_key_files = list()
        public_key_files = list()
        for i in range(public_key_count):
            public_cipher = ciphers.public_cipher(algorithm)
            private_key = public_cipher.keygen()
            public_key = private_key.public_key()
            private_key_file = 'key' + str(i) + '.key'
            public_key_file = 'key' + str(i) + '.pub'
            with open(private_key_file, 'wb') as ofstream:
                ofstream.write(private_key.export_key('PEM'))
            with open(public_key_file, 'wb') as ofstream:
                ofstream.write(public_key.export_key('PEM'))
            private_key_files.append(private_key_file)
            public_key_files.append(public_key_file)

    api.encrypt_file(plain_file, enc_file, algorithm,
                     passwords=passwords, public_key_files=public_key_files)

    if utils.is_symmetric(algorithm):
        for passwd in passwords:
            try:
                api.decrypt_file(enc_file, dec_file, password=passwd)
            except ValueError:
                print('{}: Password {} is invalid!'.format(algorithm, passwd))
                return False
    else:
        for privkey in private_key_files:
            try:
                api.decrypt_file(enc_file, dec_file, private_key_file=privkey)
            except ValueError:
                print('{}: Key file {} is invalid!'.format(algorithm, privkey))
                return False

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
    if not utils.is_symmetric(algorithm):
        for private_key_file in private_key_files:
            os.remove(private_key_file)
        for public_key_file in public_key_files:
            os.remove(public_key_file)
    return True

def main():
    """Main."""

    algorithms = [alg.name for alg in utils.AlgEnum]
    for alg in algorithms:
        print('Testing {} algorithm...'.format(alg))
        if not test(alg):
            print('\033[31m{} algorithm has not passed the test\033[0m'.format(alg))
        else:
            print('\033[32m{} algorithm has successfully passed the test\033[0m'.format(alg))

main()
