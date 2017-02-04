import sys

data = sys.stdin.read().strip().split()

assert len(data)%8 == 0

digit = {
    'ZERO' : '0',
    'ONE' : '1'
    }

data2 = []

def chunks(seq, size):
    for start in xrange(0, len(seq), size):
        chunk = seq[start:(start+size)]
        yield chunk

for chunk in chunks(data, 8):
    binary = ''.join(digit[d] for d in chunk)
    num = int(binary, base=2)
    data2.append(chr(num))

data2 = ''.join(data2)

for chunk in chunks(data2, 4):
    print chunk

