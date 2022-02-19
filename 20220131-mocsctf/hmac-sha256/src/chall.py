import os
import sys
import hmac
import hashlib

if __name__ == '__main__':
    N = 2**6

    flag = os.environ.get('FLAG', 'MOCSCTF{REDACTED}')

    inputs  = []
    outputs = []

    for _ in range(N):
        key    = bytes.fromhex(input())
        msg    = bytes.fromhex(input())
        digest = hmac.digest(key, msg, hashlib.sha256)

        inputs .append(f'{key.hex()}/{msg.hex()}')
        outputs.append(digest.hex())

    if len(set(inputs)) != N:
        print(f'brrr')
        sys.exit(-1)
    if len(set(outputs)) != 1:
        print(f'brrr')
        sys.exit(-1)

    print(f'Nice! {flag}')