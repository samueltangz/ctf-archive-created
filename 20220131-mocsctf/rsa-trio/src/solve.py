from tqdm import tqdm
from pwn import *
from math import gcd

_r = remote('localhost', 50008)

def recv():
    c = _r.recvline().decode().strip()
    if c == 'None': return None
    return int(c)

def encrypt(m):
    _r.sendlineafter(b'> ', str(m).encode())
    return recv()

# n1 = p * q
# n2 =     q * r
# n3 = p     * r

c0 = recv()

# 1. Get n3 via GCD

r_times_p = gcd(
    2**(17**3) - encrypt(2),
    3**(17**3) - encrypt(3)
)
for k in range(2, 1000):
    while r_times_p % k == 0:
        r_times_p //= k

# 2. Get n1 via binary search

lb, ub = 0, 2**2048

for _ in tqdm(range(2048)):
    m = (lb + ub) // 2
    if encrypt(m) is not None: lb = m
    else:                      ub = m

p_times_q = lb + 1

# 3. Recovering p, q, r and finishing the rest

p = gcd(p_times_q, r_times_p)
q = p_times_q // p
r = r_times_p // p

print('p =', p)
print('q =', q)
print('r =', r)

n1 = p * q
n2 = q * r
n3 = r * p

phi_n1 = (p-1) * (q-1)
phi_n2 = (q-1) * (r-1)
phi_n3 = (r-1) * (p-1)

d1 = pow(17, -1, phi_n1)
d2 = pow(17, -1, phi_n2)
d3 = pow(17, -1, phi_n3)

m = c0
m = pow(m, d3, n3)
m = pow(m, d2, n2)
m = pow(m, d1, n1)
m = m.to_bytes(2048//8, 'big').lstrip(b'\0')

print('m =', m)

_r.interactive()