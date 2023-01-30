import os
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from typing import Union
from urllib.parse import parse_qs


class AuthenticationService:
    def __init__(self, key: bytes):
        self.key = key
        self.users = {}

    def register(self, username: str, password: str) -> bool:
        if self.users.get(username) is not None: return False
        self.users[username] = password
        return True

    def signin(self, username: str, password: str) -> Union[bytes, None]:
        if self.users.get(username) != password: return None
        token = pad(f'username={username}&password={password}'.encode(), 16)
        iv = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        token = iv + cipher.encrypt(token)
        return token.hex()

    def authenticate(self, token: str) -> str:
        token = bytes.fromhex(token)
        assert len(token) % 16 == 0
        iv, c = token[:16], token[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        m = cipher.decrypt(c)
        m = unpad(m, 16)
        m = parse_qs(m.decode())

        # How do they even come to this stage and fail...? I am checking anyway.
        username, = m.get('username')
        if self.users.get(username) is None: raise Exception('Incorrect username')

        password, = m.get('password')
        if self.users.get(username) != password: raise Exception('Incorrect password')

        return username
