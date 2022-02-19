

# This file was *autogenerated* from the file gen.sage
from sage.all_cmdline import *   # import sage library

_sage_const_10 = Integer(10); _sage_const_9 = Integer(9); _sage_const_7 = Integer(7)
Zn = Zmod(_sage_const_10 **_sage_const_9  + _sage_const_7 )
P = PolynomialRing(Zn, names=('x',)); (x,) = P._first_ngens(1)

def lagrange(ys):
    n = len(ys)
    return sum(_y * product((x - x2) / (x1 - x2) for x2 in range(n) if x1 != x2) for x1, _y in enumerate(ys))

ys = list(b'MOCSCTF{th1s_pr0gr4m_1s_4lr34dy_sl0w_d01ng_ar1thm3t1c_0p3ra7i0n5}')
f = lagrange(ys)

print(f)
print(list(f))

for x, y in enumerate(ys):
    assert f(x) == y
