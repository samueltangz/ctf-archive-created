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

def connect():
    HOST = 'tertiary.pwnable.hk'
    PORT = 50013

    global debug
    if debug:
        context.log_level = 'debug'
    r = remote(HOST, PORT)
    return r

def pkey(r):
    r.sendlineafter('[cmd] ', 'pkey')
    r.recvuntil('[pkey] ')
    return int.from_bytes(base64.b64decode(r.recvline().strip()), 'big')

def read(r):
    r.sendlineafter('[cmd] ', 'read')
    r.recvuntil('[shhh] ')
    return int.from_bytes(base64.b64decode(r.recvline().strip()), 'big')

def send(r, ciphertext):
    ciphertext = int(ciphertext)
    ciphertext = int.to_bytes(ciphertext, length=(ciphertext.bit_length()+7)//8, byteorder='big')
    ciphertext = base64.b64encode(ciphertext).decode()
    r.sendlineafter('[cmd] ', f'send {ciphertext}')
    return r.recvline().strip() == b'nice'

def main():
    r = connect()

    n, e = pkey(r), 65537
    c0 = read(r)
    
    m = 1
    while True:
        print(f'[{m//2}, {m})')
        c = pow(0x80 * m + 1, e, n) * c0 % n
        if not send(r, c): break
        m *= 2

    lb, rb = m//2, m
    while lb + 1 < rb:
        print(f'[{lb}, {rb})')
        m = (lb + rb) // 2
        c = pow(0x80 * m + 1, e, n) * c0 % n
        if send(r, c): lb = m
        else:          rb = m

    print('n =', n)
    print('k =', lb)

    m = int(n // (0x80 * lb + 1))
    m = int.to_bytes(m, length=(m.bit_length()+7)//8, byteorder='big')
    print(m)


if __name__ == '__main__':
    global debug
    debug = 'debug' in os.environ

    main()