#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pwn import *
import requests
import binascii
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import hashlib
from gmpy2 import powmod
import itertools

from hash import SHA256

def connect():
    HOST = '18.163.29.56'
    PORT = 50001

    global debug
    if debug:
        context.log_level = 'debug'
    r = remote(HOST, PORT)
    return r

def spy(r, pbox, salt):
    r.sendlineafter('[cmd] ', 'spy')
    r.sendlineafter('[pbox] ', str(pbox))
    r.sendlineafter('[salt] ', base64.b64encode(salt))
    r.recvuntil('[hash] ')
    return binascii.unhexlify(r.recvline().strip())

def auth(r, password):
    r.sendlineafter('[cmd] ', 'auth')
    r.recvuntil('[pbox] ')
    pbox = eval(r.recvline())
    r.recvuntil('[salt] ')
    salt = base64.b64decode(r.recvline())
    
    permutated_password = password + salt
    permutated_password = bytes([permutated_password[pbox[i]] for i in range(20)])
    hashed_password = hashlib.sha256(permutated_password).hexdigest()
    r.sendlineafter('[hash] ', hashed_password)

def main():
    r = connect()

    h_target = spy(r, list(range(20)), b'\x00'*4)

    charset = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

    mapper = {}
    for suffix in itertools.product(charset, repeat=2):
        s = SHA256(h_target)
        s.feed(bytes(suffix) + b'\x80' + b'\x00' * 59 + b'\x02\x10')
        h = s.digest()
        mapper[h] = bytes(suffix)

    password = b''
    for i in range(8):
        h_sub = spy(r, list(range(16)) + [0x10, 0x10, 0x10, 0x10, 0x12] + [0x11] * 42 + [0x13, 2*i, 2*i + 1], b'\x00\x00\x80\xa0')
        password_part = mapper.get(h_sub)
        assert password_part is not None
        password += password_part

    auth(r, password)
    print(r.recvline().strip())    

if __name__ == '__main__':
    global debug
    debug = 'debug' in os.environ

    main()