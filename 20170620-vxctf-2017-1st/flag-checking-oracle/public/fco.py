import random
import sys
import os
import time

f = open("flag.txt", "r")
flag = f.read()

print """
Welcome to the flag checking oracle. You can check if your flag is the same as
mine! However, for sure I will not let you to brute force that easily... Enjoy.
"""

while 1:
    print "Enter your guess:"
    x = sys.stdin.readline()[:-1]
    time.sleep(0.5)
    match = True
    for i in range(len(x)):
        if x[i] != flag[i]:
            match = False
            print "Wrong! Try again."
            break
    if match == True:
        break

print "Correct!"