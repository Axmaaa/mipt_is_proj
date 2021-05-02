#!/usr/bin/python3

"""Test the application."""

import os
import secrets
import string

from algorithm import Algorithm, AlgEnum
import api

PASSWORD_ALPHABET = string.ascii_letters + string.digits
PRIVATE_KEY_FORMAT = 'PEM'
PUBLIC_KEY_FORMAT = 'PEM'


class AlgTest(): # pylint: disable=too-few-public-methods
    """Class for testing algorithm."""

    def __init__(self, algorithm):
        self.algorithm = Algorithm(algorithm)

        self.plain_file = 'file_' + self.algorithm.name + '.in'
        self.enc_file = 'file_' + self.algorithm.name  + '.enc'
        self.dec_file = 'file_' + self.algorithm.name  + '.dec'

        self.passwords = None
        self.privkey_files = None
        self.pubkey_files = None


    def __gen_text_file(self):
        """Generates random data and writes them into file."""

        data_size = 100 + secrets.randbelow(400)
        data = secrets.token_bytes(data_size)
        with open(self.plain_file, 'wb') as ofstream:
            ofstream.write(data)

    def __gen_passwords(self):
        """Generates random password."""

        self.passwords = list()
        for _ in range(3):
            pw_size = 10 + secrets.randbelow(20)
            passwd = ''.join(secrets.choice(PASSWORD_ALPHABET) for _ in range(pw_size))
            self.passwords.append(passwd)


    def __gen_key_files(self):
        """Generates key files for public-key encryption."""

        self.privkey_files = list()
        self.pubkey_files = list()
        public_cipher = self.algorithm.public_cipher()
        for i in range(3):
            private_key = public_cipher.keygen()
            public_key = private_key.public_key()
            privkey_file = 'key_' + str(i) + '.priv'
            pubkey_file = 'key_' + str(i) + '.pub'

            with open(privkey_file, 'wb') as ofstream:
                ofstream.write(private_key.export_key(PRIVATE_KEY_FORMAT))
            with open(pubkey_file, 'wb') as ofstream:
                ofstream.write(public_key.export_key(PUBLIC_KEY_FORMAT))
            self.privkey_files.append(privkey_file)
            self.pubkey_files.append(pubkey_file)


    def __check_text_file(self):
        """Checks if input file equals to decrypted file."""

        with open(self.plain_file, 'rb') as plain_ifstream:
            with open(self.dec_file, 'rb') as dec_ifstream:
                data = plain_ifstream.read()
                dec_data = dec_ifstream.read()
                if data != dec_data:
                    print('{}: Plain text is not equal to decryptes data!'
                          .format(self.algorithm.name))
                    print('{}: Plain text:     {}'.format(self.algorithm.name, data))
                    print('{}: Decrypted data: {}'.format(self.algorithm.name, dec_data))
                    return False
                return True


    def __remove_files(self):
        """Removes text and key files."""

        os.remove(self.plain_file)
        os.remove(self.enc_file)
        os.remove(self.dec_file)
        if not self.algorithm.is_symmetric():
            for private_key_file in self.privkey_files:
                os.remove(private_key_file)
            for public_key_file in self.pubkey_files:
                os.remove(public_key_file)


    def test(self):
        """Tests correctness of the algorithm encryption and decryption."""

        self.__gen_text_file()
        if self.algorithm.is_symmetric():
            self.__gen_passwords()
        else:
            self.__gen_key_files()

        api.encrypt_file(self.plain_file, self.enc_file, self.algorithm.name,
                         passwords=self.passwords, pubkey_files=self.pubkey_files)

        if self.algorithm.is_symmetric():
            for passwd in self.passwords:
                try:
                    api.decrypt_file(self.enc_file, self.dec_file, password=passwd)
                except ValueError:
                    print('{}: Password {} is invalid!'.format(self.algorithm.name, passwd))
                    return False
        else:
            for privkey in self.privkey_files:
                try:
                    api.decrypt_file(self.enc_file, self.dec_file, privkey_file=privkey)
                except ValueError:
                    print('{}: Key file {} is invalid!'.format(self.algorithm.name, privkey))
                    return False

        if not self.__check_text_file():
            return False

        self.__remove_files()

        return True

def main():
    """Main."""

    algorithms = [alg.name for alg in AlgEnum]
    for alg in algorithms:
        algtest = AlgTest(alg)
        print('Testing {} algorithm...'.format(alg))
        if not algtest.test():
            print('\033[31m{} algorithm has not passed the test\033[0m'.format(alg))
        else:
            print('\033[32m{} algorithm has successfully passed the test\033[0m'.format(alg))

main()
