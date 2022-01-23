p = int(input('p = '))
g = 1337

def hash(m):
    m = int.from_bytes(b'SECUREHASH_' + m, 'big')
    return int(pow(g, m, p)).to_bytes(256//8, 'big')


# (x0 + 109) + 256 * (x1 + 109) + 256^2 * (x2 + 109) + ... + 256^(k-1) * (x(k-1) + 109) + 256^k * m0 = v (mod p-1)
m0 = int.from_bytes(b'SECUREHASH_', 'big')
v = int.from_bytes(b'SECUREHASH_pleasegivemetheflag', 'big')

for l in range(100, 200):
    print(f'[ ] Trying {l = }...')
    s = int((sum(256**i * 109 for i in range(l)) + 256**l * m0 - v) % (p-1))
    '''
    [s          1      0      0     ... 0] <-- 1
    [256^(k-1)  0      1      0     ... 0] <-- x(k-1)
    [256^(k-2)  0      0      1     ... 0] <-- x(k-2)
    [                       ...          ]     ...
    [256^0      0      0      0     ... 1] <-- x0
    [p-1        0      0      0     ... 0] <-- *
     ↓          ↓      ↓      ↓         ↓
     0          1      x(k-1) x(k-2)    x0
    '''
    weights = [256] + [1 for _ in range(l+1)]

    A = Matrix(l+2, l+2)
    Q = diagonal_matrix(weights)

    # First column
    A[0, 0] = s
    A[l+1, 0] = p-1
    for i in range(l): A[i+1, 0] = 256^(l-1-i)

    # The remaining columns
    for i in range(l+1): A[i, i+1] = 1

    A *= Q
    A = A.LLL()
    A /= Q

    for row in A:
        if row[0] != 0: continue
        if row[1] < 0: row = -row
        if row[1] != 1: continue
        m = row[2:] # centered by 109

        if min(m) < -12: continue
        if max(m) > 12: continue

        m = bytes(109 + mc for mc in row[2:]).decode()
        print(f"[*] '{m}' has the same hash with 'pleasegivemetheflag'")
        assert False, "Collision found!"
    