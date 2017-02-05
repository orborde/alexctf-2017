# Thanks, this guy: http://stackoverflow.com/a/15391420
def isqrt(n):
    """
    >>> isqrt(1)
    1
    >>> isqrt(2)
    1
    >>> isqrt(3)
    1
    >>> isqrt(4)
    2
    >>> isqrt(5)
    2
    >>> isqrt(6)
    2
    >>> isqrt(7)
    2
    >>> isqrt(8)
    2
    >>> isqrt(9)
    3
    >>> isqrt(10)
    3
    """
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x
    
if __name__ == '__main__':
    import doctest
    fails, _ = doctest.testmod()
    assert fails == 0
