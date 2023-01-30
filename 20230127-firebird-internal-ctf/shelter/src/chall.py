import sys
import os
from Crypto.Cipher import AES
from typing import Union

from auth import AuthenticationService
from hacker import Hacker

# TODO: prevent users from trying & and = in username/password
def main():
    with open('flag.txt') as f:
        FLAG = f.read()

    key = os.urandom(16) 

    srv = AuthenticationService(key)
    hacker = Hacker(srv)

    while True:
        command, *args = input('> ').strip().split()
        if command == 'register':
            username, password = args
            if srv.register(username, password):
                print(f'🖥️  {username} registered!')
            else:
                print(f'🖥️  Cannot register {username}.')
        elif command == 'signin':
            username, password = args
            token = srv.signin(username, password)
            if token is None:
                print(f'🖥️  Cannot authenticate {username}.')
            else:
                print(f'🖥️  Signed in as {username} with token {token}.')
        elif command == 'auth':
            token, = args
            try:
                username = srv.authenticate(token)
                print(f'🖥️  The token is correct for {username}!')
            except Exception as err:
                print(f'🖥️  Invalid token: {err}.')
        elif command == 'hack':
            # I don't know why are you sending your auth token to the hacker... but there you go.
            token, = args
            try:
                srv.authenticate(token)
            except:
                print(f'😈 Stop wasting my time... This is not a valid token.')
                continue
            try:
                username, password = hacker.crack(token)
                assert srv.signin(username, password)
                print(f'😈 Thanks for sending me your token, {username}! I just got your password, {password}.')
                sys.exit(0)
            except Exception:
                print(f'😈 WHY? {FLAG}')

if __name__ == '__main__':
    main()