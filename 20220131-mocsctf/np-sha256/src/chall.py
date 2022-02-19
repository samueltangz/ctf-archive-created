import os
import sys
from sha256 import generate_hash

def main():
    m1 = bytes.fromhex(input())
    m2 = bytes.fromhex(input())

    h1 = generate_hash(m1)
    h2 = generate_hash(m2)

    if m1 == m2:
        print('No good!')
        sys.exit(-1)

    if len(m1) < 64:
        print('No good!')
        sys.exit(-1)
    if len(m2) < 64:
        print('No good!')
        sys.exit(-1)

    if h1 != h2:
        print('No good!')
        sys.exit(-1)

    flag = os.environ.get('FLAG', 'MOCSCTF{REDACTED}')
    print(f'Good! {flag}')

if __name__ == '__main__':
    main()