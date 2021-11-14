#!/usr/bin/python3

import sys
from fractions import Fraction
from functools import reduce
from operator import mul

class F:
    def __init__(self, program, n=1):
        self.program = list(map(Fraction, program))
        self.n = n

        self.terminated = False

    def step(self):
        if self.terminated: return self.n
        for k in self.program:
            n2 = self.n * k
            if n2.denominator != 1: continue
            self.n = n2.numerator

            if self.n & -self.n == self.n:
                out = chr((self.n-1).bit_length() & 0x7f)
                print(out, end='')
                sys.stdout.flush()

            return self.n
        else:
            self.terminated = True
            return self.n

def gen_primes(n):
    ps = []
    m = 3
    while len(ps) < n:
        for p in ps:
            if m % p == 0: break
        else:
            ps.append(m)        
        m += 2
    return ps

def main():
    if len(sys.argv) != 2:
        print(f'Usage: ./{sys.argv[0]} prog.frac')
        sys.exit(1)

    flag = [1] + list(input().encode())
    assert len(flag) < 100
    primes = gen_primes(len(flag))
    n = reduce(mul, [p**k for p, k in zip(primes, flag)])

    with open('prog.frac') as f:
        prog = f.read().strip().split('\n')

    f = F(prog, n)

    while not f.terminated:
        f.step()

if __name__ == '__main__':
    main()