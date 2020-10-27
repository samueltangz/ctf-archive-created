from Crypto.PublicKey import RSA
import os

iv = int(os.urandom(2).encode("hex"), 16)

f = open('pubkey.pem','r')
public_key = RSA.importKey(f.read())

f = open("flag.txt", "r")
flag = f.read()

prev = iv
for i in range(0, len(flag), 2):
    m = prev ^ int(flag[i : i + 2].encode("hex"), 16)
    c = pow(m, public_key.e, public_key.n)
    prev = c
    print c
