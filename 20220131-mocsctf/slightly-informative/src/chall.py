from Crypto.Util.number import getPrime as get_prime

def main():
    with open('flag.txt', 'rb') as f:
        m = int.from_bytes(f.read(), 'big')

    p, q = [get_prime(512) for _ in 'pq']
    n = p * q
    phi_n = (p-1) * (q-1)

    e = 0x10001
    d = pow(e, -1, phi_n)

    c = pow(m, e, n)

    # Leaking dp = d % (p-1) would lead to a wildly Google-able CTF challenge...
    # How about s and t such that d = s*p + t?
    s = d // p
    t = d % p

    print(f'{n = }')
    print(f'{e = }')
    print(f'{c = }')
    print(f'{s = }')
    print(f'{t = }')

if __name__ == '__main__':
    main()