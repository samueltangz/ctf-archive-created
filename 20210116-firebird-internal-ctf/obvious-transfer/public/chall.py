from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import long_to_bytes
import base64
import random

from secret import flag

def long_to_b64(payload):
    return base64.b64encode(long_to_bytes(payload)).decode()

def main():
    k = RSA.generate(2048)
    oaep_k = PKCS1_OAEP.new(k)

    failed = False
    exited = False

    print('🔑', long_to_b64(k.n))

    for i in range(1, 100+1):

        c0 = random.getrandbits(1)

        print(f'🤯 {i}')

        while True:
            params = input('🤖 ').split(' ')
            action = params.pop(0)

            if action == '📦':
                if c0 == 0:
                    ciphertext = random.randint(0, k.n-1)
                else:
                    ciphertext = int.from_bytes(oaep_k.encrypt(flag), 'big')
                print('🤫', long_to_b64(ciphertext))
            elif action == '🔓':
                c1 = int(params[0])
                if c0 != c1:
                    failed = True
                else:
                    print('👌')
                break
            elif action == '🏃':
                exited = True
                break
        if failed or exited: break

    if exited:
        print('👋')
    elif failed:
        print('🤨')
    else:
        print('🏁', flag.decode())


if __name__ == '__main__':
    main()

