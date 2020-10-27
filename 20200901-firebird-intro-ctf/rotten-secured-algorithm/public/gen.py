# Challenge written on Aug 26, 2020 by Mystiz.

from Crypto.PublicKey import RSA
import random
import time
from datetime import datetime
from secret import flag

t = int(time.time())

assert len(flag) < 256

k = RSA.generate(1024)

p, q = k.p, k.q

n = p * q
e = random.randrange(2**1024) * (p-1) * (q-1) + 1

m = f'''
This message is encrypted on {datetime.fromtimestamp(t)}.
I have crafted the public key - it is so secure that no one is able to recover this message ever.
But wait, you said you did? Then take this flag - {flag} and get away. I mean congrulations!
'''.strip().encode()

m = int.from_bytes(m, 'big')
c = pow(m, e, n)

print('n =', hex(n))
print('e =', hex(e))
print('c =', hex(c))
