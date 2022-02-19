(9)
Sign in Please 請登入
500 Points / 1 Solves

# Author

Blackb6a

# Solver

T0022 Member 3

# Description

I have implemented a secure authentication system. You can't eavesdrop the passwords, can you?

我發明了一個安全的身份驗證系統。反正沒有人能竊聽密碼吧。

nc tertiary.pwnable.hk 50001

# Files

chall.py

# Analyze

Basically, the challenge is asking for the answer (``auth``) to the hash given the ``pbox`` and the ``salt``, which we do not know in advance.

Also, we are given the function (``spy``) to test out the hash calculated using our input (``pbox`` and ``salt``) and the unknown ``password``.

The whole string to test is 20-byte long, which composes of the random ``password`` (16 bytes) generated at the beginning of the connection and the ``salt`` (4 bytes), and the string gets shuffled by the given ``pbox``.

```python
def permutate(payload, pbox):
    return bytes([payload[x] for x in pbox])
```

Simply speaking, it is returning ``[payload[pbox[0]], payload[pbox[1]], payload[pbox[2]], ..., payload[pbox[len(pbox) - 1]]]`` in the form of bytes.

Notice that the ``permutate`` process only retrieves the characters with the index given in the ``pbox``, it does not check for the length of the ``pbox``, or any repetition in the ``pbox``.

So initially I would think that it would be useful using a rainbow table to recover the ``password``.

The 16-byte ``password`` is generated by encoding a random 12-byte integer using base64, so only the 64 characters used in base64 (``"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"``)  are possible to appear in the ``password`` part.

For example, if we send $[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]$ as the ``pbox``, it is supposed to permutate the ``payload`` to a 2-distinct(1-if-duplicated)-character-only string ($[p[0], p[1], p[0], p[1], ...]$), which generated hash can be checked against our rainbow table of every "2-character combination repeated 10 times" (only $64×64=4096$ combinations) to obtain the first 2 characters of the password.

We have only 10 iterations available to test, so at least 2 characters have to be recovered per iteration to recover the password.

A program is created to test this type of ``pbox``, but 'no way!' in the exception part appears.

To find out the issues, we can see that there is a verification check to the ``pbox``.

```python
assert len(set(pbox)) == 20
assert len(salt) == 4
```

It means that we can only use 4 characters for the ``salt``, and ``pbox`` should contain exactly 20 different integers as indices.

I was wondering if I can use different integers to obtain the same element from the ``payload`` array. The only possible integers I can think of is negative indices for counting from the end (e.g. 2 and -18 corresponding to the same element in a 20-byte payload)

However, we only have control over the 4-byte salt. So at most we can use 8 bytes for the known characters in the payload, and the remaining 12 bytes are in the password, thus at least 6 elements have to be loaded from the password part.
(e.g. ``pbox`` = $[0, 1, 2, 3, 4, 5, 16, 17, 18, 19, -1, -2, -3, -4, -15, -16, -17, -18, -19, -20]$)
To create a rainbow table for 6 characters, we have to store $64^6 = 2^{36} = 68719476736$ values which takes so much time which makes this method impractical.

So the idea of negative indices is abandoned.

So it seems that our last resort is the SHA256 algorithm.

SHA256, which generates a 256-bit hash as indicated in the name, algorithm breaks the ``payload`` into 512-bit (64-byte) blocks. The initial hash array is a 256-bit constant split into 8 parts for calculation. The initial hash array for the next block is the hash calculated from the previous block. As it seems that the default ``hashlib`` library does not provide the feature to use custom initial hash values, so I crafted my ``SHA256`` library according to the SHA-2 documentation.

Before the calculation, the ``payload`` is first padded to the length of a multiple of 512 bits (64 bytes). A ``'1'`` bit is appended to the ``payload`` first, then ``'0'`` bits are appended until there are still 64 bits to a multiple of 512 ($\text{length} \equiv 448\ (\text{mod }512)$), then the 64-bit representation of the length of the payload (in bits) is added at the end.

For the default 20-byte payload, the padded payload should appear as below:
```
+---------------------+------------------+-------------------------------+------------------+
| the 20-byte payload | 128 (0b10000000) | 42-bytes of null (0b00000000) | 160 (0b10100000) |
+---------------------+------------------+-------------------------------+------------------+
```
where $160\text{ bits} = 20 × 8\text{ bits}$, and 128 is equivalent to a ``'1'`` bit and 7 ``'0'`` bits.

Therefore, if a length extension attack is carried out to calculate the hash, we have to use the second block.

Also, the content of the first block should not be modified in order to have a known initial hash.
which means, we need chr(128), chr(0) and chr(160) in the ``salt`` in order to have the pbox-permutated result containing these bytes.
The order is not important for the ``pbox``, so by default we can use
$[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]$
as after pbox-permuatation the order of the ``payload`` remains the same (and so the first 16-byte is the ``password`` we want, which is convenient to us).

Therefore, we carry out our first test using 
$[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]$
as the ``pbox``, and the ``salt`` explained below (which is not important in this stage).

(Notice that the ``assert`` check only checks for 20 distinct values in ``pbox``, but not repeating elements, so we can definitely send a ``pbox`` of more than 20 elements as the input.)

The hash returned is the initial hash array of the 2nd block in SHA256.

To construct the 2nd block that contains our desired value, we would like to use 2 bytes from the password as the start of this block, so each time we can recover 2 bytes of the password after comparing the returned hash from the system to our rainbow table.

The structure of the 2nd block:
```
+----+----+
| p1 | p2 |
+----+----+
```
where $p1$ and $p2$ are the tested part of the password.
The padded block should appear as below: (Notice that in total we have to send a $512 + 2 × 8 = 210_{16}$ bits string).
```
+----+----+------------------+-------------------------------+----------------+-----------------+
| p1 | p2 | 128 (0b10000000) | 59-bytes of null (0b00000000) | 2 (0b00000010) | 16 (0b00010000) |
+----+----+------------------+-------------------------------+----------------+-----------------+
```
The block size is $1 + 1 + 1 + 59 + 1 + 1 = 64\text{ bytes}\ (= 512\text{ bits})$

Therefore, the rainbow table is generated using the tested hash received from the server as the initial hash, and
$[c1] + [c2] + [128] + [0] × 59 + [2, 16]$
, where $[c1]$ and $[c2]$ are substituted by each possible pairs of characters in base64, as the padded payload.

Notice that to achieve that, we have to disable the padding procedure of the SHA256 function, which also seems to be impossible with the default python ``hashlib`` library.

After generating the hash table, the next step is to send the ``pbox`` and ``salt``.

The supposed content of the ``payload`` after permutated by the ``pbox`` is $p1$ and $p2$ appended just after the first block.
Also, as mentioned before, the ``pbox`` can be much longer as long as exactly 20 different elements are found in it.
Besides, the ``salt`` has to be crafted carefully so we can have chr(128), chr(0) and chr(160) in the permutated ``payload``.

My chosen ``salt`` is $[0, 160, 2, 128]$ (2 is not used as the input actually)

The custom ``pbox`` is created as follows to construct desired pre-padded ``payload``:

$[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]$ + $[19]$ (corresponding to 128) + $[16]$ (corresponding to null bytes) $×\ 42$ + $[17]$ (corresponding to 160) + $[n, n+1]$ (the two characters in password we crack)
in these 8 iterations, we have to test all the 16 characters in ``password``, so n corresponds to $[0, 2, 4, 6, 8, 10, 12, 14]$ in these 8 iterations.

After receiving the 8 hashes and comparing them to the rainbow table, the ``password`` is recovered, and we have only 1 allowed iteration left.

Therefore, we have to do the authentication this time.

The system provides a random ``pbox`` and ``salt``. We can directly copy the functions (``parse_pbox`` and ``permutate``) in the given source code to calculate the permutated ``payload`` and the required hash value, and send it to the server.

After that, the flag should be shown if nothing is wrong. Solved.

## Example Output

```
AKACgA==
b'\x00\xa0\x02\x80'
4
[x] Opening connection to tertiary.pwnable.hk on port 50001
[x] Opening connection to tertiary.pwnable.hk on port 50001: Trying 18.163.58.67
[+] Opening connection to tertiary.pwnable.hk on port 50001: Done
b'[cmd] '
b'[pbox] '
b'[salt] '
b'935229df4a638142892d4d18601258858fc1bee30fbec9ce6fa28e5a47d39edd'
b'[cmd] '
b'[pbox] '
b'[salt] '
b'[cmd] '
b'[pbox] '
b'[salt] '
b'[cmd] '
b'[pbox] '
b'[salt] '
b'[cmd] '
b'[pbox] '
b'[salt] '
b'[cmd] '
b'[pbox] '
b'[salt] '
b'[cmd] '
b'[pbox] '
b'[salt] '
b'[cmd] '
b'[pbox] '
b'[salt] '
b'[cmd] '
b'[pbox] '
b'[salt] '
b'[cmd] '
b'[pbox] '
b'[salt] '
b'[hash] '
b'[flag] hkcert20{d0_y0u_feel_s3cur3_wh3n_s19nin9_in?}\n'
[*] Closed connection to tertiary.pwnable.hk port 50001
```

The source code is given in the Walkthrough Part.

# Walkthrough (Codes)
sign in.py (the comments are used to test whether my library works properly)
```python
from pwn import *
import base64, sha256, os
import hashlib

# rainbow table
salt = bytes([0, 160, 2, 128])
salt64 = base64.b64encode(salt).decode()

# test extension
#print(sha256.sha_256("a"*1))
#print(sha256.sha_256(b"a" + bytes([128]) + b"\0" * 61 + bytes([8]) + b"b", True, True))
#print(sha256.sha_256(b"b" + bytes([128]) + b"\0" * 60 + b"\2" + bytes([8]), False, True, i=sha256.sha_256("a"*1)))
#passwordt = base64.b64encode(os.urandom(12))
#print(passwordt + salt)
#init1 = sha256.sha_256(passwordt + salt, byts = True)
#print(sha256.bytes2string(init1))
#init2 = sha256.sha_256(passwordt + salt + bytes([128]) + b'\0' * 42 + bytes([160]) + b'ab', byts = True)
#print(sha256.bytes2string(init2))
#print(sha256.bytes2string(sha256.sha_256(b'ab' + bytes([128]) +  b'\0' * 59 + bytes([2, 16]), pads = False, byts = True, i=init1)))

print(salt64)
print(base64.b64decode(salt64))
print(len(base64.b64decode(salt64)))
rainbow = [""] * (64*64)
def parse_pbox(payload):
    return list(map(int, payload[1:-1].split(',')))


def permutate(payload, pbox):
    return bytes([payload[x] for x in pbox])

per = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/" 


r = remote('tertiary.pwnable.hk', 50001)

password = ""
# get 1 block hash
print(r.recvuntil('[cmd] '))
r.sendline("spy")
print(r.recvuntil('[pbox] '))
r.sendline(str([i for i in range(20)]))
print(r.recvuntil('[salt] '))
r.sendline(salt64)
r.recvuntil('[hash] ')
password = r.recvuntil('\n')[:-1]
print(password)
# break password into bytes
password = [int(password[i:i+8],16) for i in range(0,len(password),8)]

# rainbow table
for ic in range(64):
    for jc in range(64):
        i = per[ic]
        j = per[jc]
        rainbow[ic * 64 + jc] = sha256.bytes2string(sha256.sha_256((i + j).encode() + bytes([128]) + b'\0' * 59 + bytes([2, 16]), False, True, password))
real = ""
for j in range(8):
    print(r.recvuntil('[cmd] '))
    r.sendline("spy")
    print(r.recvuntil('[pbox] '))
    r.sendline(str([i for i in range(20)] + [19] + [16] * 42 + [17] + [j*2, j*2+1]))
    print(r.recvuntil('[salt] '))
    r.sendline(salt64)
    r.recvuntil('[hash] ')
    result = r.recvuntil('\n')[:-1]
    ind = rainbow.index(result.decode())
    real += per[ind // 64] + per[ind%64]
    
print(r.recvuntil('[cmd] '))
r.sendline("auth")
print(r.recvuntil('[pbox] '))
pbox = parse_pbox(r.recvuntil('\n')[:-1].decode())
print(r.recvuntil('[salt] '))
salt = base64.b64decode(r.recvuntil('\n')[:-1])
print(r.recvuntil('[hash] '))
permutated_password = permutate(real.encode() + salt, pbox)
r.sendline(hashlib.sha256(permutated_password).hexdigest())
print(r.recvuntil('\n'))
r.close()
```

sha256.py
```python
initial_hash_values=[
0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19
]

sha_256_constants=[
0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')
def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

def pad(a, pads=True, byts=False):
    le = len(a) << 3
    if byts:
        a = int_from_bytes(a)
    else:
        a = int_from_bytes(a.encode())
    if pads:
        a = (a << 1) + 1
        a = (a << (512 - (le + 65)%512))
        a = (a << 64) + le
    else:
        if le%512 > 0:
            a = (a << (512 - le%512))
    s = hex(a)[2:]
    s = ("0" * 128 + s)[-((len(s)-1)-(len(s)-1)%128+128):]
    #print(s)
    return [int(s[i:i+8],16) for i in range(0,len(s),8)]

INT_MAX = (1 << 32) - 1

def rr(i, p):
    return (INT_MAX & (i << (32-p))) | (i >> p) 

def sha_256(s, pads=True, byts=False, i=initial_hash_values):
    ha = i.copy()
    W = [0] * 64
    bi = pad(s, pads, byts)
    for i in range(0, len(bi), 16):
        a, b, c, d, e, f, g, h = ha
        for j in range(64):
            if j < 16:
                W[j] = bi[j+i]
                #print(j, W[j])

            else:
                w = W[j-15]
                s0 = rr(w, 7) ^ rr(w, 18) ^ (w >> 3)
                w = W[j-2]
                s1 = rr(w, 17) ^ rr(w, 19) ^ (w >> 10)
                # print(s0, s1)
                W[j] = INT_MAX & (W[j-16] + s0 + W[j-7] + s1)
                # print(W[j])
                # input()
            S0 = rr(a, 2) ^ rr(a, 13) ^ rr(a, 22)         
            S1 = rr(e, 6) ^ rr(e, 11) ^ rr(e, 25)
            ch = (e & f) ^ ((INT_MAX - e) & g)
            temp1 = INT_MAX & (h + S1 + ch + sha_256_constants[j] + W[j])
            #print(temp1)
            maj = (a&b)^(a&c)^(b&c)
            temp2 = INT_MAX & (S0 + maj)
            #print(temp2)

            h, g, f, e, d, c, b, a = g, f, e, INT_MAX & (d + temp1), c, b, a, INT_MAX & (temp1 + temp2)
            #print(a,b,c,d,e,f,g,h)
            #input()
        ha = [INT_MAX & (ha[k] + [a,b,c,d,e,f,g,h][k]) for k in range(8)]
    return ha
    
def bytes2string(b):
    s = ""
    for i in range(8):
        s += ("0" * 8 + hex(b[i])[2:])[-8:]
    return s    
```

# Provided Source File(s)

chall.py
```python
# Challenge written by Mystiz.
# Signature: PHNjcmlwdD5jb25zb2xlLmxvZygnVEhJUyBDSEFMTEVOR0UgSVMgV1JJVFRFTiBGT1IgSEtDRVJUIENURiBBTkQgSVMgTk9UIEZPUiBGUkFOS0lFIExFVU5HIFRPIFBMQUdBUklaRS4nKTwvc2NyaXB0Pg==

import base64
import hashlib
import os
import random

from secret import flag


def parse_pbox(payload):
    return list(map(int, payload[1:-1].split(',')))


def permutate(payload, pbox):
    return bytes([payload[x] for x in pbox])


class Server:
    def __init__(self, password):
        assert len(password) == 16
        self.password = password

    def preauth(self):
        pbox = list(range(20))
        salt = os.urandom(4)
        random.shuffle(pbox)
        return pbox, salt

    def auth(self, pbox, salt, hashed_password):
        permutated_password = permutate(self.password + salt, pbox)
        return hashlib.sha256(permutated_password).hexdigest() == hashed_password


class Client:
    def __init__(self, password):
        self.password = password

    def spy(self, pbox, salt):
        assert len(set(pbox)) == 20
        assert len(salt) == 4
        password = self.password
        permutated_password = permutate(password + salt, pbox)

        hashed_password = hashlib.sha256(permutated_password).hexdigest()
        print(f'[hash] {hashed_password}')


def main():
    password = base64.b64encode(os.urandom(12))

    s = Server(password)
    c = Client(password)

    for _ in range(10):
        command = input('[cmd] ')
        try:
            if command == 'spy':
                pbox = parse_pbox(input('[pbox] '))
                salt = base64.b64decode(input('[salt] '))
                c.spy(pbox, salt)
            elif command == 'auth':
                pbox, salt = s.preauth()
                print(f'[pbox] {pbox}')
                print(f'[salt] {base64.b64encode(salt).decode()}')
                hashed_password = input('[hash] ')
                if not s.auth(pbox, salt, hashed_password):
                    raise Exception('No!')
                print(f'[flag] {flag}')
        except:
            print('no way!')


if __name__ == '__main__':
    main()
```

# Flag

``hkcert20{d0_y0u_feel_s3cur3_wh3n_s19nin9_in?}``

Do you feel secure when signing in?