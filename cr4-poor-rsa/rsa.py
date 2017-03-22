def inverse(a, n):
    t = 0
    newt = 1;    
    r = n
    newr = a;    
    while newr != 0:
        quotient = r / newr
        t, newt = (newt, t - quotient * newt) 
        r, newr = (newr, r - quotient * newr)
    if r > 1:
        assert False
    if t < 0:
        t = t + n
    return t

def powmod(x, p, mod):
    xsqp = x
    val = 1
    while p > 0:
        do = (p & 1)
        if do:
            val *= xsqp
            val = (val % mod)
        p /= 2
        xsqp *= xsqp
        xsqp = (xsqp % mod)
    return val

def compute_d(e, phi):
    return inverse(e, phi)

def decrypt(c, d, n):
    return powmod(c, d, n)
