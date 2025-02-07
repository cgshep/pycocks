import gmpy2

def hex_to_mpz(h):
    return gmpy2.mpz(int(h, 16))


def str_to_mpz(s):
    """
    Convert a string to a gmpy2.mpz integer.

    The string is first encoded into bytes using UTF-8, and then
    the bytes are interpreted as a big-endian integer.

    Args:
        s (str): The input string.

    Returns:
        mpz: The resulting arbitrary-precision integer.
    """
    # Encode the string into bytes
    byte_data = s.encode('utf-8')

    # Convert the bytes to an integer (big-endian)
    integer_value = int.from_bytes(byte_data, byteorder='big')

    # Return the integer as a gmpy2.mpz object
    return gmpy2.mpz(integer_value)


def mpz_to_hex(m):
    return hex(m)[2:]


def mpz_to_str(x):
    """
    Convert a gmpy2.mpz integer to a string.

    The mpz integer is first converted to a Python int, then to a bytes object
    (using big-endian order), and finally decoded into a UTF-8 string.

    Args:
        x (mpz): The input arbitrary-precision integer.

    Returns:
        str: The resulting string.
    """
    # Convert mpz to a Python int
    x_int = int(x)

    # Determine the number of bytes needed to represent x_int.
    # For x_int = 0, bit_length() returns 0 so we handle that case separately.
    nbytes = (x_int.bit_length() + 7) // 8
    if nbytes == 0:
        return ""

    # Convert the integer to a bytes object.
    byte_data = x_int.to_bytes(nbytes, byteorder='big')

    # Decode the bytes to a UTF-8 string.
    return byte_data.decode('utf-8')


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
