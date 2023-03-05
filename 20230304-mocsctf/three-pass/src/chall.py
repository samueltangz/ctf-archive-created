'''
You are the person-in-the-middle between Alice and Bob's communication. This is
how Alice sends a message, m, to Bob securely:

     Alice                          Bob
     =====                         =====

      [m]

   Encrypts
the message m

         ------E(m, kA)------->
   
                                 Encrypts
                               the message
                                 E(m, kA)
   
         <---E(E(m, kA), kB)---

    Decrypts
  the message
E(E(m, kA), kB)

         ------E(m, kB)------->

                                 Decrypts
                               the message
                                 E(m, kB)
   
                                   [m]
'''

import os
from gmpy2 import is_prime
import random
from math import gcd

# Returns a 1024-bit prime
def get_prime():
    while True:
        p = int.from_bytes(os.urandom(1024//8), 'big') | (1<<1023)
        if is_prime(p): return p

p, q = [get_prime() for _ in 'pq']
n = p * q

phi_n = (p-1) * (q-1)

while True:
    e_a = random.randint(1, phi_n)
    if gcd(e_a, phi_n) == 1: break
while True:
    e_b = random.randint(1, phi_n)
    if gcd(e_b, phi_n) == 1: break

d_a = pow(e_a, -1, phi_n)
d_b = pow(e_b, -1, phi_n)

print(f'{n = }')
print(f'{e_a = }')
print(f'{e_b = }')

#  ------ m^e_a ----->
#  <-- m^(e_a*e_b) ---
#  ------ m^e_b ----->

with open('flag.txt', 'rb') as f: m = f.read()

m = int.from_bytes(m, 'big')
c1 = pow(m, e_a, n)
print(f'{c1 = }')

c2 = pow(c1, e_b, n)
print(f'{c2 = }')

c3 = pow(c2, d_a, n)
print(f'{c3 = }')

c4 = pow(c3, d_b, n)
assert c4 == m
