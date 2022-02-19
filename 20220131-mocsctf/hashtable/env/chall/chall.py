import os
import time
from hashtable import HashTable

def main():
    secret_hidden  = False
    secret_key     = os.urandom(16)
    secret_message = b'no flag for you'

    flag = os.environ.get('FLAG', 'MOCSCTF{REDACTED}')

    ht = HashTable()
    while True:
        try:
            cmd = input('> ').split(' ')
            if cmd[0] == 'set':
                key = bytes.fromhex(cmd[1])
                value = bytes.fromhex(cmd[2])
                ht.add(key, value)
            elif cmd[0] == 'get':
                key = bytes.fromhex(cmd[1])
                res = ht.find(key)
                if res == False: continue
                print(res)
            elif cmd[0] == 'delete':
                key = bytes.fromhex(cmd[1])
                ht.delete(key)

            elif cmd[0] == 'put_secret':
                ht.add(secret_key, secret_message)
                secret_hidden = True
            elif cmd[0] == 'get_secret':
                if secret_hidden == False:
                    print('Go hide the secret first!')
                elif ht.find(secret_key) != secret_message:
                    print(f'You overwrote the key! This is your flag: {flag}')
                else:
                    print('Try harder!')

        except KeyboardInterrupt:
            raise KeyboardInterrupt

if __name__ == '__main__':
    main()