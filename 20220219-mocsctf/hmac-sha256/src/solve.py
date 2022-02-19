from pwn import *

r = remote('localhost', 50004)

for k in range(64):
    r.sendline(b'00'*k)
    r.sendline()

r.interactive()