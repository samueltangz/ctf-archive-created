import sys
import string
import random

from rc4 import RC4
from secret import flag


def prefix_length(u, v):
    for i in range(len(u)):
        if u[i] == v[i]: continue
        return i
    else:
        return len(u)

def convert_key(s):
    return [ord(c) for c in s]

def encrypt(cipher, message):
    return ''.join([chr(ord(message[i]) ^ next(cipher)) for i in range(len(message))])

def main():
    charset = string.ascii_letters + string.digits
    key1 = ''.join(random.choices(charset, k=16))    
    print('🔑', key1)

    key2 = input('🔑 ')

    if key1 in key2:
        print('🤨')
        sys.exit(0)

    key1 = convert_key(key1)
    key2 = convert_key(key2)

    cipher1 = RC4(key1)
    cipher2 = RC4(key2)

    ciphertext1 = encrypt(cipher1, flag)
    ciphertext2 = encrypt(cipher2, flag)
    l = prefix_length(ciphertext1, ciphertext2)

    if l == 0:
        print('🤨')
        sys.exit(0)
    elif l != len(flag):
        print(f'🏁 {flag[:l]}...')
    else:
        print(f'🏁 {flag[:l]}')

if __name__ == '__main__':
    main()

