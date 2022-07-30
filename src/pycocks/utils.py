import gmpy2

def hex_to_mpz(h):
    return gmpy2.mpz(int(h, 16))


def str_to_mpz(s):
    return hex_to_mpz(s.encode().hex())


def mpz_to_hex(m):
    return hex(m)[2:]


def mpz_to_str(m):
    return bytes.fromhex(mpz_to_hex(m)).decode()


def hash_mpz(a, f):
    a = mpz_to_hex(a)
    a = f(bytes(a, "utf-8")).hexdigest()
    a = hex_to_mpz(a)
    return a


class DecryptionFailure(Exception):
    pass


class ExtractFailure(Exception):
    pass


class InvalidMessageType(Exception):
    pass


class InvalidIdentityString(Exception):
    pass
