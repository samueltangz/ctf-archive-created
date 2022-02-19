import os

class RC4:
    def __init__(self, key):
        keylength = len(key)

        s = [i for i in range(256)]

        j = 0
        for i in range(256):
            j = (j + s[i] + key[i % keylength]) % 0xff
            s[i], s[j] = s[j], s[i]

        self.i = 0
        self.j = 0
        self.s = s

    def __next(self):
        s, i, j = self.s, self.i, self.j

        i = (i + 1)    % 0xff
        j = (j + s[i]) % 0xff

        s[i], s[j] = s[j], s[i]

        self.s, self.i, self.j = s, i, j

        return s[(s[i] + s[j]) % 0xff]

    def encrypt(self, message):
        return bytes(m^self.__next() for m in message)

if __name__ == '__main__':
    key = os.urandom(16)
    cipher = RC4(key)

    flag = os.environ.get('FLAG', 'MOCSCTF{REDACTED}').encode()

    while True:
        command = input()
        if command == 'flag':
            print(cipher.encrypt(flag).hex())
        elif command.startswith('message '):
            message = bytes.fromhex(command.split(' ')[1])
            print(cipher.encrypt(message).hex())
        else:
            print('Invalid command')

    '''
    Usage:
    - "flag"
      Returns the encrypted flag
    - "message 74657374696e67"
      Returns the encrypted message "testing"
    '''