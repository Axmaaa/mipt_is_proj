#!/usr/bin/python3

"""Main."""

import api

passwds = [
    'qwerty123',
    'payalnik',
    'slozhnyy_parol'
    ]

plain_file = 'file.in'
enc_file = 'file.enc'
dec_file = 'file.dec'

api.encrypt_file(plain_file, enc_file, 'aes', passwds)
print('File was encrypted')

passwd = input('Input password: ')
try:
    api.decrypt_file(enc_file, dec_file, passwd)
except ValueError:
    print('Invalid password!')
else:
    print('File was decrypted')
