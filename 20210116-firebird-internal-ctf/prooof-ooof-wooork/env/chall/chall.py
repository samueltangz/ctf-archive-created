import base64
import random
import signal
import sys

import fenwick_tree

charset = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890'
flag = 'firebird{r3m3mb3r_n0t_t0_7ru5t_4ny0n3}'

def xor(a, b):
    return bytes([u^v for u, v in zip(a, b)])

class Random:
    def __init__(self, seed):
        self.state = seed

    def next(self):
        self.state = (0x1337 * self.state + 0x5) & 0xffffffff
        return self.state

# ========

def attempt(seed, rounds, cs):
    N = 100000

    state = [0 for _ in range(N)]
    r = Random(seed)
    ms = b''
    for c in cs:
        for _ in range(rounds):
            x, y = [r.next() % N for _ in range(2)]
            z = r.next()
            if x > y: x, y = y, x

            for k in range(x, y):
                state[k] += z
                state[k] &= 0xff

        x, y = [r.next() % N for _ in range(2)]
        if x > y: x, y = y, x

        ms += bytes([(sum(state[x:y]) & 0xff) ^ c])
    return ms

def fast_attempt(seed, rounds, cs):
    N = 100000

    ft1 = [0 for _ in range(N+1)]
    ft2 = [0 for _ in range(N+1)]

    rng = Random(seed)
    ms = b''
    for c in cs:
        for _ in range(rounds):
            l, r = [rng.next() % N for _ in range(2)]
            z = rng.next()
            if l > r: l, r = r, l

            fenwick_tree.update_range(ft1, ft2, N, z, l, r-1)

        l, r = [rng.next() % N for _ in range(2)]
        if l > r: l, r = r, l

        out = fenwick_tree.range_sum(l, r-1, ft1, ft2) & 0xff
        ms += bytes([out ^ c])
    return ms

# ========

def tle_handler(*kwargs):
    print('Too slow!')
    sys.exit(0)

def generate_attempt(seed, rounds, length):
    x = fast_attempt(seed, rounds, b'\0'*length)
    while True:
        m = bytes(random.choices(charset, k=length))
        c = xor(x, m)
        
        if b'\0' not in c: break

    challenge = base64.b64encode(c).decode()

    return challenge, m.decode()


def main():
    signal.alarm(180)
    signal.signal(signal.SIGALRM, tle_handler)

    print('This challenge is easy. Just execute the binary to complete the proof-of-work!')
    print('Of course, it will be getting harder and harder...')

    k_special = random.randint(20, 50)

    for k in range(100):
        # Generate an input without NULL byte
        seed = random.getrandbits(32)
        rounds = (k+1)**2

        challenge, solution = generate_attempt(seed, rounds, 10)
        if k == k_special:
            challenge = base64.b64encode(solution.encode()).decode()
            print(f'touch /tmp/.wallofshame && echo {challenge} | base64 -d')
        else:
            print(f'./gen {challenge} {seed} {rounds}')
        res = input('> ')

        if res != solution: break
    else:
        print(f'Congraulations! You have make it through the 100 stages! Here is your flag: {flag}')


# For testing only and will not used in deployment
def test():
    from tqdm import tqdm

    # Speed test
    for k in tqdm(range(100)):
        seed = random.getrandbits(32)
        rounds = (k + 1)**2
        fast_attempt(seed, rounds, b'\0'*10)

    # Correctness
    for k in tqdm(range(100)):
        seed = random.getrandbits(32)
        rounds = 5 * (k + 1)
        assert attempt(seed, rounds, b'\0'*10) == fast_attempt(seed, rounds, b'\0'*10)


if __name__ == '__main__':
    # test()
    main()

