import binascii
import sys
import numpy as np
import base64

def vxhash(m):
    val = 0xdeadbeefdeadbeef
    for x in m:
        val *= 257
        val += ord(x)
        val &= 0xffffffffffffffff
    return val

f = open("flag.txt")
g = f.read()

print """This program is to ensure you really know the flag.
Please input the flag:"""

m = sys.stdin.readline()[:-1]

hashm = format(vxhash(base64.b64encode(m)), 'x')
hashg = format(vxhash(base64.b64encode(g)), 'x')

print hashm
if len(m) < 7:
    print "Seriously, you do think the flag that short?"
elif len(m) > 100:
    print "Seriously, you do think the flag that long?"
elif m[0:6] != 'vxctf{' or m[-1] != '}':
    print "I do think you know the format of the flag..."
elif hashm == hashg:
    print "Okay, I know you really know the flag!\nI think I may want to show you again because the flag is awesome:\n%s" % g
else:
    print "Stop pretending, this is not the real flag!\nThe checksum of the flag is %s, not %s." % (hashg, hashm)