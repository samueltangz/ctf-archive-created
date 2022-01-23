from gmpy2 import is_prime
from math import gcd
from pwn import *

r = process(['python3', 'chall.py'])
# r = remote('localhost', 50001)

solver = process(['sage', 'collide.sage'])

def hash(m):
    r.sendline(m.encode())
    r.recvuntil(b' = ')
    return int(r.recvline().decode(), 16)


g97  = hash('a') # g^97 mod p
g98  = hash('b') # g^98 mod p
g99  = hash('c') # g^99 mod p
g100 = hash('d') # g^100 mod p

# g98^2 = g97 * g99 mod p
p = gcd(g98**2 - g97*g99, g99**2 - g98*g100)
for k in range(2, 10000):
    while p % k == 0:
        p //= k

assert is_prime(p)

log.success(f'Prime found: {p}')

solver.sendlineafter(b'p =', str(p).encode())
solver.recvuntil(b"'")
m = solver.recvuntil(b"'")[:-1]

log.success(f'Message that collides: {m}')

r.sendline(m)
r.interactive()