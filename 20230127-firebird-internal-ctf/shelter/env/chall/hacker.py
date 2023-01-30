from Crypto.Util.Padding import unpad
from urllib.parse import parse_qs

def xor(a, b):
    return bytearray(u^v for u, v in zip(a, b))
    
class Hacker:
    def __init__(self, srv):
        # The function to check if the padding is correct
        self.srv = srv

    def __oracle(self, token):
        try:
            self.srv.authenticate(token.hex())
            return True
        except Exception as err:
            return str(err) not in [
                'Padding is incorrect.',
                'PKCS#7 padding is incorrect.'
            ]


    def __recover_block(self, ciphertext_block):
        iv = bytearray(16)

        for k in range(16):
            for i in range(256):
                iv[15-k] = i
                crafted_iv = xor(iv, bytes([k+1 for _ in range(16)]))
                if self.__oracle(crafted_iv + ciphertext_block): break
        return iv

    def __recover(self, ciphertext):
        return b''.join([
            xor(ciphertext[i-16:i],
                self.__recover_block(ciphertext[i:i+16]))
            for i in range(16, len(ciphertext), 16)
        ])
    
    def crack(self, token):
        token = bytes.fromhex(token)
        m = self.__recover(token)
        m = unpad(m, 16)
        m = parse_qs(m.decode())

        username, = m.get('username')
        password, = m.get('password')

        return username, password
