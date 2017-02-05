import sys

values = [int(line) for line in sys.stdin.read().splitlines()]
values.sort()
print len(values), 'analyzed'
print 'min', min(values)
print 'max', max(values)

import math
print 'maxbits', max(math.log(n)/math.log(2) for n in values)
