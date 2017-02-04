import sys

data = sys.stdin.read().strip().split()

assert len(data)%8 == 0

digit = {
    'ZERO' : '0',
    'ONE' : '1'
    }

data2 = []
for start in xrange(0, len(data), 8):
    chunk = data[start:(start+8)]
    binary = ''.join(digit[d] for d in chunk)
    num = int(binary, base=2)
    data2.append(chr(num))

print ''.join(data2)


