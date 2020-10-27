# Library: pycrypto
import random

def gcd(a, b):
    while b > 0:
        a = a % b
        a, b = b, a
    return a

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

from Crypto.PublicKey import RSA

m = "Hey guys, vxctf{5orry_1_r3u53d_th3_pr1m35} for this problem :("
flag = int(m.encode("hex"), 16)

# Generate key with n being 2048 bits
key_r = RSA.generate(2048)

u = 0
v = 0
while u == v:
    u = random.randint(0, 499)
    v = random.randint(0, 499)

generated = 0
while generated < 500:
    key = RSA.generate(2048)
    if generated == u or generated == v:
        public_key = RSA.construct((key.p * key_r.p, 65537))
        q = key_r.p
    else:
        q = key.q
    n = key.p * q
    public_key = RSA.construct((n, 65537))
    if gcd(key.p - 1, key.e) > 1 or gcd(q - 1, key.e) > 1:
        continue
    d = modinv(key.e, (key.p - 1) * (q - 1))

    c = pow(flag, key.e, n)
    print "n = %d\ne = %d\nc = %d\n" % (n, key.e, c)
    if hex(pow(c, d, n))[2:-1].decode("hex") != m:
        print "a" * 1024

    generated += 1
