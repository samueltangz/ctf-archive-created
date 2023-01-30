from Crypto.PublicKey import RSA
import random

random.seed(1337)

key = RSA.generate(2048)

t = [(key.p>>random.getrandbits(10))&1 if random.getrandbits(1) else (key.q>>random.getrandbits(10))&1 for i in range(2048)]
t = sum(t[i]<<i for i in range(2048))

with open('flag.txt', 'rb') as f:
    m = int.from_bytes(f.read(), 'big')

n, e = key.n, key.e
c = pow(m, e, n)

print(f'{n = }')
print(f'{e = }')
print(f'{t = }')
print(f'{c = }')