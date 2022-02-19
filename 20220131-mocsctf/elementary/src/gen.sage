Zn = Zmod(10^9 + 7)
P.<x> = PolynomialRing(Zn)

def lagrange(ys):
    n = len(ys)
    return sum(_y * product((x - x2) / (x1 - x2) for x2 in range(n) if x1 != x2) for x1, _y in enumerate(ys))

ys = list(b'MOCSCTF{th1s_pr0gr4m_1s_4lr34dy_sl0w_d01ng_ar1thm3t1c_0p3ra7i0n5}')
f = lagrange(ys)

print(f)
print(list(f))

for x, y in enumerate(ys):
    assert f(x) == y