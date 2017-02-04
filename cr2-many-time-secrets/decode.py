# Python's string.printable with some of the obviously unprintable
# stuff deleted (I think this is as weird a comment as you do.)
PRINTABLE_BYTES = set(
    b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!'
    b'"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n')
def is_printable(vec):
    """Does this byte vector represent an ASCII printable string?"""
    return all(c in PRINTABLE_BYTES for c in vec)


def chunks(seq, size):
    for start in range(0, len(seq), size):
        chunk = seq[start:(start+size)]
        yield chunk


lines = []
data = []

for line in open('msg', 'r'):
    line = line.strip()
    print(line, len(line))
    line = [int(digit, base=16) for digit in chunks(line, 2)]
    lines.append(line)
    data.extend(line)

print()

def code(d, x):
    return d^x

def bytes2binary(bytearr):
    """
    >>> bytes2binary(bytes([120, 10, 2]))
    '011110000000101000000010'
    """
    return ''.join(bin(b)[2:].zfill(8) for b in bytearr)

def xorvec_helper(a, b):
    assert(len(a) == len(b))
    return bytes((x ^ y) for x,y in zip(a,b))

def xorvec(*args):
    """XORs bytes() objects together"""
    output = args[0]
    for n in args[1:]:
        output = xorvec_helper(output, n)
    return output


def hamming_distance(a, b):
    """
    >>> hamming_distance(b'this is a test', b'wokka wokka!!!')
    37
    """
    assert(len(a) == len(b))
    diff = bytes2binary(xorvec(a, b))
    return diff.count("1")

def repeating_key_group(key_length, seq):
    """
    >>> repeating_key_group(2, range(11))
    [(0, 2, 4, 6, 8), (1, 3, 5, 7, 9)]
    >>> repeating_key_group(2, b'abcdefg')
    [(97, 99, 101), (98, 100, 102)]
    """
    iters = [iter(seq)]*key_length
    return list(zip(*zip(*iters)))

# Frequency table cribbed from
# http://en.algoritmy.net/article/40379/Letter-frequency-English
ENGLISH_LETTER_FREQUENCIES=[
    ['A', '8.167'],
    ['B', '1.492'],
    ['C', '2.782'],
    ['D', '4.253'],
    ['E', '12.702'],
    ['F', '2.228'],
    ['G', '2.015'],
    ['H', '6.094'],
    ['I', '6.966'],
    ['J', '0.153'],
    ['K', '0.772'],
    ['L', '4.025'],
    ['M', '2.406'],
    ['N', '6.749'],
    ['O', '7.507'],
    ['P', '1.929'],
    ['Q', '0.095'],
    ['R', '5.987'],
    ['S', '6.327'],
    ['T', '9.056'],
    ['U', '2.758'],
    ['V', '0.978'],
    ['W', '2.360'],
    ['X', '0.150'],
    ['Y', '1.974'],
    ['Z', '0.074']
    ]
ENGLISH_LETTER_FREQUENCIES = dict(
    (letter.encode(), float(val)/100)
    for letter,val in ENGLISH_LETTER_FREQUENCIES)

def english_letters_metric(vec):
    """Score a candidate plaintext by the sum of the frequencies of
    its letters.
    """
    vec = vec.upper()
    valid_letters = bytearray(
        c for c in vec if (bytes([c]) in ENGLISH_LETTER_FREQUENCIES))
    if len(valid_letters) == 0:
        return 0
    score = (
        sum(ENGLISH_LETTER_FREQUENCIES[bytes([c])] for c in valid_letters))
    return score

import math

ENGLISH_LETTERS_LOG_FREQUENCIES = dict(
    (letter, math.log(val))
    for letter,val in ENGLISH_LETTER_FREQUENCIES.items())
def english_letters_log_metric(vec):
    """ TODO: Explain me. Multinomial distribution, logspace, yadda yadda. """
    vec = vec.upper()
    return sum(vec.count(letter) * val
               for letter,val in ENGLISH_LETTERS_LOG_FREQUENCIES.items())

def xorchar(char, vec):
    """XORs a single byte (int 0-255) against an entire byte array."""
    # Kind of a silly way of doing this, but why write more for loops
    # when you can use the one you already wrote?
    return xorvec(bytes([char]*len(vec)), vec)

def xorbytes(key, vec):
    key_repeats = len(vec) // len(key) + 1  # approximately :-)
    key_vec = (key * key_repeats)[:len(vec)]
    return xorvec(key_vec, vec)


def crack_xorchar(vec, metric=english_letters_log_metric):
    """Attempts to crack the xorchar "encryption" applied to byte array 'vec'"""
    decrypts = [(c, xorchar(c, vec)) for c in range(256)]
    decrypts.sort(key=lambda t: metric(t[1]))
    decrypts.reverse()
    return decrypts


import functools
def prod(iterable):
    return functools.reduce(lambda x,y: x*y, iterable, 1)


def xorbytes_printable_keyspace(key_length, ciphertext):
    def search(block):
        decrypts = crack_xorchar(block)
        for k, d in decrypts:
            if is_printable(bytes([k])) and is_printable(d):
                yield english_letters_metric(d), k

    blocks = [bytearray(g) for g in repeating_key_group(key_length, ciphertext)]
    solnsets = [list(search(b)) for b in blocks]
    return solnsets

def countkeys(keyspace):
    return prod([len(seq) for seq in keyspace])

gibberish = bytes(data)
candidates = []
for length in range(1,50):
    # Chop up into groups. Drop the last one.
    reduced_length = (len(gibberish) // length) * length
    groups = list(chunks(gibberish[:reduced_length], length))
    pairs = zip(groups[:-1], groups[1:])
    norm_distances = [hamming_distance(a,b)/length for a,b in pairs]
    avg_dist = sum(norm_distances) / len(norm_distances)
    #print(length, avg_dist, len(gibberish) / length)
    candidates.append((avg_dist, length))
candidates.sort()
print('Lowest-Hamming 5:')
for dist, length in candidates[:5]:
    print(length, dist)

_, length = candidates[0]
print('Choosing key length', 29)
keyspace = xorbytes_printable_keyspace(length, gibberish)
assert(countkeys(keyspace) > 0)
print('Length', length)
print(countkeys(keyspace), 'possible keys.')
[l.sort(reverse=True) for l in keyspace]
bestkey = bytes(max(l)[1] for l in keyspace)
print('Highest scoring key:', bestkey)
print('First three lines of plaintext:')
for line in xorbytes(bestkey, gibberish).decode().splitlines()[:3]:
    print('>', line)
print()

key=b'ALEXCTF{HERE_GOES_THE_KEY}'
print(len(key))
for line in lines:
    print(xorbytes(key, line))

