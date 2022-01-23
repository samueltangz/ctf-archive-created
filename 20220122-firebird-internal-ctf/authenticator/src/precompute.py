from tqdm import tqdm
import itertools
from blake3 import blake3 # https://pypi.org/project/blake3/

suffix = b"HANDSHAKE_FROM_SERVER" + b'\0'*16

f = open('precomputed.bin', 'wb')

charset = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# HANDSHAKE_FROM_SERVER
for ptuple in tqdm(itertools.product(
    charset,
    charset,
    charset,
    charset,
    charset,
    b'0',
), total=62**5):
    password = bytes(ptuple)
    f.write(blake3(password + suffix).digest()[:8])