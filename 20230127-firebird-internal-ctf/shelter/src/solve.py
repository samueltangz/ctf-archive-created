from pwn import *

r = remote('carbon-chal.firebird.sh', 36013)

r.sendline(b'register foo xxxxxxxx\x02')
# username=foo&password=xxxxxxxx\x02

tokens = []
while len(tokens) == 0:
    for _ in range(1024):
        r.sendline(b'signin foo xxxxxxxx\x02')

    for _ in range(1024):
        r.recvuntil(b'Signed in as foo with token ')
        token = bytes.fromhex(r.recvuntil(b'.')[:-1].decode())
        
        if token[30] != 1: continue
        if token[31]^0x1^0x2 > token[31]: continue
        tokens.append(token.hex())

token = tokens[0]
print(f'{token = }')
r.sendline(f'hack {token}'.encode())
r.recvuntil(b'WHY? ')

r.interactive()
