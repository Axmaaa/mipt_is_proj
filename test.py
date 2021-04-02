#!/usr/bin/python3

"""Main."""

import enum

import header
import caesar

class Algorithm(enum.Enum):
    """The enum contains the codes of the algorithms."""

    CAESAR = enum.auto()

# Read passwords
passwords = list()
with open('passwords.txt', 'r') as ifstream:
    for line in ifstream:
        passwords.append(line[:-1])

# Set header
hdr = header.Header()

algorithm = 'CAESAR'
for alg in Algorithm:
    if algorithm == alg.name:
        hdr.algorithm = alg.value

hdr.users_count = len(passwords)

key = caesar.keygen()

for password in passwords:
    hdr.add_user(False, password, key)

with open('plain.txt', 'rb') as fin:
    with open('caesar.enc', 'wb') as fout:
        hdr.write(fout)
        caesar.encrypt(fin, fout, key)

hdr = header.Header()
with open('caesar.enc', 'rb') as fin:
    hdr.read(fin)
    passwd = input('Input password: ')
    try:
        key = hdr.key(passwd)
    except ValueError:
        print('Invalid password!')
    else:
        with open('caesar.dec', 'wb') as fout:
            caesar.decrypt(fin, fout, key)
