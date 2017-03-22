MODULUS="""
    52:a9:9e:24:9e:e7:cf:3c:0c:bf:96:3a:00:96:61:
    77:2b:c9:cd:f6:e1:e3:fb:fc:6e:44:a0:7a:5e:0f:
    89:44:57:a9:f8:1c:3a:e1:32:ac:56:83:d3:5b:28:
    ba:5c:32:42:43
"""

MODULUS = MODULUS.strip()

def desplit(s, d):
    return ''.join(s.split(d))

MODULUS = desplit(desplit(MODULUS, '\n    '), ':')
print MODULUS

n = int(MODULUS, base=16)
print n

print 'Trying low divisors'
for i in range(2, 100000):
    if (n % i) == 0:
        print i, (n / i)


print 'Trying sqrt'
from maths import *
sq = isqrt(n)
if sq*sq == n:
    print 'Square root matched:', sq

sqsq = sq*sq
if sqsq > n:
    print 'sqrt^2 > n'
elif sqsq < n:
    print 'sqrt^2 < n'
else:
    print 'sqrt^2 == n'

ssqssq = (sq+1)*(sq+1)
if ssqssq > n:
    print 'sqrt^2 > n'
elif ssqssq < n:
    print 'sqrt^2 < n'
else:
    print 'sqrt^2 == n'

for q in range(sq - 20, sq + 20 + 1):
    if (n % q) == 0:
        print q


print 'Trying some Mersennes'
for p in range(2, 2000):
    maysenne = 2 ** p - 1
    if (n % maysenne) == 0:
        print p, maysenne, n / p

print 'Maybe the modulus is just p?'
import rsa
e=65537
p = n
phi = (p - 1)

flagdata = open('flag.bin', 'rb').read()
c = 0
for q in flagdata:
    q = ord(q)
    c *= 256
    c += q
print 'c =',hex(c)
d = rsa.compute_d(e, phi)
print 'd =',hex(d)
m = rsa.decrypt(c, d, n)
print 'm =',hex(m)

