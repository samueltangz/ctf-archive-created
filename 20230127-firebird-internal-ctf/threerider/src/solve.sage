import random
import re
from Crypto.Cipher import AES
from Crypto.Util import Counter
from operator import mul
from functools import reduce

#                      f i r e b i r d {                                                                                                           }
known = bytes.fromhex('ffffffffffffffffff8080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080ff')
m =     bytes.fromhex('66697265626972647b00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007d')
c =     bytes.fromhex('f84bf7049cb55a0e1457d977e6cfbc0cc49ee1102da505e10aa3c32e619180446617ae2270cba3629b0851ae627236f19bb9cbfcadcd010eb923d170cbc2a7')

def xor(a, b):
    return bytes([u^^v for u, v in zip(a, b)])

keystreams = []
for k in range(256):
    cipher = AES.new(bytes([k]) + b'\0'*15, AES.MODE_CTR, counter=Counter.new(128, initial_value=int(0)))
    keystreams.append(
        cipher.encrypt(b'\0'*len(c))
    )

A = []
b = []

# The number of entries I guessed that they are zeroes
# Suggested: sampled_zeroes + number_of_equations >= 256 (or add some more to avoid less false positives...)

number_of_equations = bin(int.from_bytes(known, 'big')).count('1')
sampled_zeroes = 256 - number_of_equations
assert sampled_zeroes <= 256-16
print(f'{sampled_zeroes + number_of_equations = }')

for i, (rc, mc, cc) in enumerate(zip(known, m, c)):
    for j in range(8):
        if (rc>>j) & 1 == 0: continue
        mb = (mc>>j) & 1
        cb = (cc>>j) & 1

        row = [(k[i]>>j) & 1 for k in keystreams]

        A.append(row)
        b.append(mb^^cb)

F = GF(2)
A = Matrix(F, A)
b = vector(F, b)

hit_frequency = reduce(mul, [(256-16-k)/(256-k) for k in range(sampled_zeroes)])
print(f'{number_of_equations = }')
print(f'{sampled_zeroes = }')
print(f'Expecting a hit every {int(1/hit_frequency)} times')

attempt = 0
while True:
    attempt += 1

    # The 128 entries "I" guessed it is non-zero
    v = sorted(random.sample(range(256), k=256-sampled_zeroes))
    
    _A = A[:, v]
    try:
        x0 = _A.solve_right(b)
        for dx in _A.right_kernel():
            flag = c
            set_bits_count = 0
            for i in range(256-sampled_zeroes):
                if x0[i] == dx[i]: continue
                set_bits_count += 1
                flag = xor(flag, keystreams[v[i]])

            flag = flag.decode()
            if not re.match(r'firebird\{\w+\}', flag): continue
            if set_bits_count > 16: continue

            print(f'[*] Flag recovered at attempt #{attempt}: {flag}')
            assert False, 'done!'

    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except AssertionError as err:
        raise err
    except:
        pass
