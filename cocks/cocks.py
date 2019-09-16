"""
This is a Python implementation of Cocks' identity-based encryption (IBE) system.

Helpful resources:
1. C. Cocks, "An Identity Based Encryption Scheme Based on Quadratic Residue",
   Proc. 8th IMA Int'l Conf. on Cryptography and Coding, 2001
2. "Cocks IBE scheme", Wikipedia, https://en.wikipedia.org/wiki/Cocks_IBE_scheme
"""

import random
import gmpy2
import logging

import bitarray

from bitarray import bitarray
from hashlib import sha512
from cocks.utils import *

__author__ = "Carlton Shepherd"

prng = random.SystemRandom()
random_state = gmpy2.random_state()
logger = logging.getLogger()

class CocksPKG:
    def __init__(self, n_len=2048, f=sha512):
        """
        Initialises the Cocks public key generator (PKG).

        Input:
        n_len : Modulus size
        f : Hash function for iteratively hashing ID values.
        """
        self.n_len = n_len
        self.f = f
        self.setup()

    def _gen_prime(self, n_bits):
        """
        Generates an n-bit prime.
        
        Input:
        n_bits : Desired prime size (in bits)
        
        Output:
        n-bit prime
        """
        n = gmpy2.mpz(prng.getrandbits(n_bits))
        return gmpy2.next_prime(n)

    def setup(self):
        """
        Generates two distinct primes, p and q, both of which are both congruent
        to 3 mod 4, and its product, n, which is the scheme's modulus.
        """
        n = 0
        while n.bit_length() != self.n_len:
            p = q = 0
            while p % 4 != 3:
                p = self._gen_prime(self.n_len // 2)
            while p == q or q % 4 != 3:
                q = self._gen_prime(self.n_len // 2)
            n = p * q
        self.p = p
        self.q = q
        self.n = n
        self.f = sha512

    def extract(self, id_str):
        """
        Extracts a user's private key from their identity string.

        If necessary, the ID string, a, is hashed iteratively until (a|n)==1.
        
        Input:
        id_str : Identity string
        
        Output:
        r : User's secret key
        a : Hashed identity value such that (a | n) == 1
        """
        if id_str == "" or id_str == None:
            raise InvalidIdentityString("Invalid user identity string")

        id_mpz = str_to_mpz(id_str)
        a = hash_mpz(id_mpz, self.f)
        a_tmp = 0

        while gmpy2.jacobi(a_tmp, self.n) != 1:
           a_tmp = hash_mpz(a_tmp, self.f)
        a = a_tmp

        logging.debug(f"Jacobi (a/n) = {gmpy2.jacobi(a, self.n)}")
        logging.debug(f"Jacobi (-a/n) = {gmpy2.jacobi(-a, self.n)}")
        
        r = pow(a, (self.n + 5 - (self.p+self.q)) // 8, self.n)
        r2 = (r*r) % self.n

        logging.debug(f"a = {a % self.n}")
        logging.debug(f"-a = {-a %self.n}")
        logging.debug(f"r = {r}")
        logging.debug(f"r**2 = {r2}")

        if r2 != (a % self.n) and r2 != (-a % self.n):
            raise ExtractFailure(
                "Error deriving r: r^2 != a (mod n) and r^2 != -a (mod n)!")
        return (r, a)


class Cocks:
    def __init__(self, n):
        """
        Initialises the Cocks scheme (user-side).

        Input:
        n : Public modulus generated by the PKG
        """
        self.n = n

    def _encrypt_bit(self, m_bit, a):
        """
        Encrypts an individual message bit.

        Inputs:
        m_bit : Message bit in {-1,1}
        a : Hashed identity value

        Output:
        (c1, c2) : Ciphertext tuple
        """
        t1 = t2 = gmpy2.mpz_random(random_state, self.n)

        while gmpy2.jacobi(t1, self.n) != m_bit:
            t1 = gmpy2.mpz_random(random_state, self.n)

        while gmpy2.jacobi(t2, self.n) != m_bit or t1 == t2:
            t2 = gmpy2.mpz_random(random_state, self.n)

        c1 = (t1 + a * gmpy2.invert(t1, self.n)) % self.n
        c2 = (t2 - a * gmpy2.invert(t2, self.n)) % self.n
        return (c1, c2)

    def encrypt(self, msg, a):
        """
        Encrypts a byte array message.
        
        Input:
        msg : Message as a byte array
        a : Hashed identity value

        Output:
        c_list : List of ciphertext tuples for each encrypted bit
        """
        if type(msg) != bytes:
            raise InvalidMessageType(
                f"Expected msg with bytes type, but got {type(msg)}")

        x = bitarray() ; x.frombytes(msg)
        # Transform message space: {0,1} -> {-1,1}
        msg_arr = [1 if b else -1 for b in x] 
        return [self._encrypt_bit(b, a) for b in msg_arr]

    def _decrypt_bit(self, c1, c2, r, a):
        """
        Decrypts an individual message bit from a ciphertext tuple,
        given the user's private key and their hashed ID value.

        Inputs:
        (c1, c2) : Ciphertext tuple
        r : User's secret key
        a : Hashed identity value

        Output:
        (x|n) : Decrypted message bit in {-1,1}
        """

        r2 = (r*r) % self.n
        x = c1 + 2*r if r2 == a else c2 + 2*r
        return gmpy2.jacobi(x, self.n)

    def decrypt(self, c_list, r, a):
        """
        Decrypts a list of ciphertext tuples to a byte array.

        Inputs:
        c_list : List of ciphertext tuples
        r : User's secret key
        a : Hashed identity value

        Output:
        x : Decrypted byte array
        """
        bit_list = [self._decrypt_bit(c1, c2, r, a) for (c1, c2) in c_list]
        # Transform message space: {-1,1} -> {0,1}
        msg_arr = [0 if b < 0 else b for b in bit_list]
        x = bitarray(msg_arr)
        return x.tobytes()