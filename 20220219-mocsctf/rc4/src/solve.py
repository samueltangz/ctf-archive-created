from pwn import *

r = remote('localhost', 50006)

u = set()

while len(u) < 255:
    r.sendline('message ' + '00'*1024)
    u |= set(bytes.fromhex(r.recvline().decode()))

missing = 255*256//2 - sum(u)

r.sendline('flag')
c0 = bytes.fromhex(r.recvline().decode())

candidates = [set() for _ in c0]

while any(len(c) < 255 for c in candidates):
    r.sendline('flag')
    c0 = bytes.fromhex(r.recvline().decode())
    
    for i, c in enumerate(c0):
        candidates[i].add(c)

flag = bytes([missing ^ (255*256//2 - sum(c)) for c in candidates])
print(flag)

r.interactive()