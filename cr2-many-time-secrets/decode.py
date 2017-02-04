def chunks(seq, size):
    for start in xrange(0, len(seq), size):
        chunk = seq[start:(start+size)]
        yield chunk


data = []

for line in open('msg', 'r'):
    line = line.strip()
    line = [int(digit, base=16) for digit in chunks(line, 2)]
    data.extend(line)


