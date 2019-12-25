import random
import sys
import os

seed = int(os.urandom(4).encode("hex"), 16)

def nextRandomBit():
    global seed
    val = 1
    for i in range(32):
        if seed & (1 << i):
            val ^= 1
    seed = (seed << 1) & 0xffffffff | val
    return val

def nextRandomInt():
    val = 0
    for i in range(16):
        val = val * 2 + nextRandomBit()
    return val

vals = [0] * 5
for i in range(5):
    vals[i] = str(nextRandomInt())

print """
   ____     _     ___               __           ___                  ___ ___ 
  / __/__  (_)___/ _ \___ ____  ___/ /__  __ _  / _ \___  ___ _  _  _<  // _ \\
 / _// _ \/ / __/ , _/ _ `/ _ \/ _  / _ \/  ' \/ , _/ _ \/ _ `/ | |/ / // // /
/___/ .__/_/\__/_/|_|\_,_/_//_/\_,_/\___/_/_/_/_/|_/_//_/\_, /  |___/_(_)___/ 
   /_/                                                  /___/                 

Welcome to EpicSecureRng, the only TRUE random-number generator in the world!
We are glad to introduce a bounty challenge: If you could predict the next TEN
numbers in the sequence, you win $1,000,000 instantly!

The first five numbers are %s.""" % (", ".join(vals))

for i in range(10):
    print "%d down! What is the next number?" % i
    if int(sys.stdin.readline()) != nextRandomInt():
        print "Haha! I told you that ERRng is totally random. Didn't I?"
        sys.exit()

print "You are correct! You must be so lucky..."
f = open("flag.txt", "r")
print f.read()