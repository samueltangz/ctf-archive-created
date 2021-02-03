from Crypto.PublicKey import RSA
from gmpy2 import is_prime
import random

from secret import flag

def gen_prime(bits=1024):
    while True:
        p = 2**(bits-1) + sum([2**random.randint(1, bits-1) for i in range(6)]) + 1
        if is_prime(p): return p

p, q = [gen_prime() for _ in range(2)]
n = p * q
e = 0x10001
m = int.from_bytes(flag, 'big')
c = pow(m, e, n)

print('n =', n)
print('e =', e)
print('c =', c)