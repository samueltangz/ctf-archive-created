import json

with open('output.json') as f:
    j = json.loads(f.read())

c, e, n = map(int, [j['c'], j['e'], j['n']])

'''
p = 2 * 2^1022 + p0
q = 3 * 2^1022 + q0

p*q = (2 * 2^1022 + p0) * (3 * 2^1022 + q0)
    = 6 * 2^2044 + 2 * 2^1022 * q0 + 3 * 2^1022 * p0 + p0*q0
'''

v = int(n % 2^1022)

u = int(n // 2^1022 % 2^1022)
if u >= 2^1021: u -= 2^1022

# TODO: Check the case when v < 0
P.<x> = PolynomialRing(ZZ)

# x = p0, y = q0
# / 3*x + 2*y = u
# \ x*y = v
# 2*x*y = 2*v => x*(u-3*x) = 2*v

f = x * (u - 3*x) - 2*v
for p0, _ in f.roots():
    p = 2 * 2^1022 + p0
    if n % p == 0: break
else:
    assert False, "no solution"

q = n // p

phi_n = (p-1) * (q-1)
d = int(pow(e, -1, phi_n))

m = pow(c, d, n)
flag = int.to_bytes(m, (m.bit_length()+7)//8, 'big')
print(f'{flag = }')
