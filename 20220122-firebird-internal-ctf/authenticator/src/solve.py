from pwn import *
from tqdm import tqdm
from blake3 import blake3

def connect():
    return process(['python3', 'chall.py'])

charset = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
def reconstruct_password(id):
    steps = [1, 62, 62, 62, 62, 62]
    r = []
    for step in steps:
        r.append(charset[id % step])
        id //= step
    return bytes(rc for rc in r)[::-1]

assert reconstruct_password(0)  == b'000000'
assert reconstruct_password(1)  == b'000010'
assert reconstruct_password(8)  == b'000080'
assert reconstruct_password(62) == b'000100'


def attempt(r):
    r.sendlineafter(b'challenge_client = ', b'00000000000000000000000000000000')

    r.recvuntil(b'response_server = ')
    response_server = bytes.fromhex(r.recvline().decode())

    r.recvuntil(b'challenge_server = ')
    challenge_server = bytes.fromhex(r.recvline().decode())

    if response_server[:8] not in content: raise Exception('not found')
    index = content.find(response_server[:8])
    if index % 8 != 0: raise Exception('not found')
    password = reconstruct_password(index//8)

    response_client = blake3(password + b"HANDSHAKE_FROM_CLIENT" + challenge_server).digest()
    r.sendlineafter(b'response_client = ', response_client.hex().encode())

    res = r.recvline().strip()
    if res.startswith(b'\x1b[031m'): raise Exception(res)

    return res


try:
    p = log.progress('Loading precomputed digests')
    # This thing is like 8GB...
    with open('precomputed.bin', 'rb') as f:
        content = f.read()
    p.success('Done!')
except Exception as err:
    log.error(str(err))
    raise err

# It is expected to get flag in 62 attempts with precomputing 62^5 entries.
for _ in tqdm(range(1000)):
    try:
        r = connect()
        res = attempt(r)
        print(res)
        break
    except KeyboardInterrupt:
        break
    except:
        r.close()
else:
    print(f'Too harsh! Cannot get flag in 1000 tries.')