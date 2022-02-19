from gmpy2 import is_prime
import os

flag = os.environ.get('FLAG', 'MOCSCTF{REDACTED}').encode()
flag = int.from_bytes(flag, 'big')
e = 0b10001

def generate_prime():
    while True:
        p = int.from_bytes(os.urandom(1024//8), 'big')
        if p % e == 1: continue
        if p.bit_length() != 1024: continue
        if not is_prime(p): continue
        return p

def encrypt(m, ns):
    c = m
    for n in ns:
        if not 0 <= c < n: return None
        c = pow(c, e, n)
    return c

def main():
    p, q, r = [generate_prime() for _ in 'rsa']
    ns = sorted([p*q, q*r, r*p])

    print(encrypt(flag, ns))
    
    while True:
        m = int(input('> '))
        c = encrypt(m, ns)
        print(c)

if __name__ == '__main__':
    main()
