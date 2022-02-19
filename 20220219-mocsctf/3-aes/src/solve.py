from pwn import *
from Crypto.Cipher import AES
import base64
import hashlib
from tqdm import tqdm


def xor(a, b):
    return bytes(u^v for u, v in zip(a, b))

def encrypt_flag():
    r.sendlineafter(b'> ', b'2')
    r.recvuntil(b': ')
    return base64.b64decode(r.recvline())

def encrypt(m):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b': ', base64.b64encode(m))
    r.recvuntil(b': ')
    return base64.b64decode(r.recvline())


r = remote('localhost', 50001)
# r = process(['python3', 'chall.py'])

c_flag = encrypt_flag()

# Recover key and IV
c = encrypt(b'\0'*48)

r.close()

c1 = c[ 0:16]
c2 = c[16:32]
c3 = c[32:48]

m1 = b'\0'*16
m2 = b'\0'*16
m3 = b'\0'*16

for _key in tqdm(range(2**24)):
    # Brute force the keys
    key = int.to_bytes(_key, 3, 'big')
    key = hashlib.md5(key).digest()

    cipher = AES.new(key, AES.MODE_ECB)

    c2_xor_s3 = cipher.decrypt(c3)
    s3 = xor(c2_xor_s3, c2)

    c1_xor_s2 = cipher.decrypt(c2)
    s2 = xor(c1_xor_s2, c1)

    s2_xor_r3 = cipher.decrypt(s3)
    r3 = xor(s2_xor_r3, s2)

    r2_xor_m3 = cipher.decrypt(r3)
    r2 = xor(r2_xor_m3, m3)

    r1_xor_m2 = cipher.decrypt(r2)
    r1 = xor(r1_xor_m2, m2)

    iv_xor_m1 = cipher.decrypt(r1)
    iv = xor(iv_xor_m1, m1)

    iv_xor_r1 = xor(iv, r1)
    s1 = cipher.encrypt(iv_xor_r1)

    iv_xor_s1 = xor(iv, s1)
    _c1 = cipher.encrypt(iv_xor_s1)

    if c1 != _c1: continue

    flag = c_flag
    for _ in range(3):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        flag = cipher.decrypt(flag)
    print(f'{flag = }')
