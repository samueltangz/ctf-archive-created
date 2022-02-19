from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.Padding import pad, unpad
from hashlib import md5
import base64
import os
import signal

keys = [list()] * 3

def gen_keys():
    for i in range(len(keys)):
        key = md5(os.urandom(3)).digest()
        iv = md5(os.urandom(6)).digest()
        keys[i].append(key)
        keys[i].append(iv)

def encrypt(m: bytes) -> bytes:
    assert len(m) % 16 == 0
    c = m
    for key_iv in keys:
        cipher = AES.new(key_iv[0], mode=AES.MODE_CBC, iv=key_iv[1])
        c = cipher.encrypt(c)
    return c

def decrypt(c: bytes) -> bytes:
    assert len(c) % 16 == 0
    m = c
    for key_iv in keys:
        cipher = AES.new(key_iv[0], mode=AES.MODE_CBC, iv=key_iv[1])
        m = cipher.decrypt(m)
    return m

signal.alarm(120)

def main():

    gen_keys()

    while True:
        print("===== MENU =====")
        print("1. Encrypt your plaintext")
        print("2. Get encrypted flag")
        op = int(input("> "))

        if op == 1:
            plaintext = base64.b64decode(input("Please input your plaintext (base64): "))
        elif op == 2:
            plaintext = os.environ.get('FLAG', 'MOCSCTF{REDACTED}').encode()
        else:
            exit()

        ciphertext = encrypt(pad(plaintext, 16))
        assert unpad(decrypt(ciphertext), 16) == plaintext
        print("Here's your ciphertext: {}".format(base64.b64encode(ciphertext).decode()))

if __name__ == "__main__":
    main()