import gmpy2
import pytest

from pycocks.utils import InvalidIdentityString
from pycocks.cocks import CocksPKG, Cocks


def test_encrypt_decrypt():
    m1 = bytes(b"Hello")
    m2 = bytes("Hello world", encoding="utf8")
    m3 = bytes(12345)
    m4 = bytes(b"aaaaaaaaaaa bbbbbbbbbbbb cccccccccc dddddddddd")
    m5 = bytes("Lorem ipsum dolor sit amet, consectetur"\
               "adipiscing elit, sed do eiusmod tempor incididunt"\
               "ut labore et dolore magna aliqua. Ut enim ad"\
               "minim veniam, quis nostrud exercitation ullamco"\
               "laboris nisi ut aliquip ex ea commodo consequat."\
               "Duis aute irure dolor in reprehenderit in"\
               "voluptate velit esse cillum dolore eu fugiat "\
               "nulla pariatur. Excepteur sint occaecat cupidatat"\
               "non proident, sunt in culpa qui officia deserunt"\
               "mollit anim id est laborum.", encoding="utf8")
    cocks_pkg = CocksPKG()
    test_id = "test"
    r, a = cocks_pkg.extract(test_id)
    cocks = Cocks(cocks_pkg.n)
    c_list = cocks.encrypt(m1, a)
    assert m1 == cocks.decrypt(c_list, r, a)
    c_list = cocks.encrypt(m2, a)
    assert m2 == cocks.decrypt(c_list, r, a)
    c_list = cocks.encrypt(m3, a)
    assert m3 == cocks.decrypt(c_list, r, a)
    c_list = cocks.encrypt(m4, a)
    assert m4 == cocks.decrypt(c_list, r, a)
    c_list = cocks.encrypt(m5, a)
    assert m5 == cocks.decrypt(c_list, r, a)


def test_pkg_modulus():
    # Test modulus bit lengths.
    # Caution: this will take some time.
    cocks_pkg = CocksPKG()
    assert cocks_pkg.n.bit_length() == 2048
    cocks_pkg = CocksPKG(512)
    assert cocks_pkg.n.bit_length() == 512
    cocks_pkg = CocksPKG(1024)
    assert cocks_pkg.n.bit_length() == 1024
    cocks_pkg = CocksPKG(3072)
    assert cocks_pkg.n.bit_length() == 3072
    cocks_pkg = CocksPKG(4096)
    assert cocks_pkg.n.bit_length() == 4096


def test_pkg_extract():
    cocks_pkg = CocksPKG()
    _, a = cocks_pkg.extract("test")
    assert gmpy2.jacobi(a, cocks_pkg.n) == 1
    _, a = cocks_pkg.extract("012345678938")
    assert gmpy2.jacobi(a, cocks_pkg.n) == 1
    _, a = cocks_pkg.extract("this is a longer user identity string")
    assert gmpy2.jacobi(a, cocks_pkg.n) == 1
    _, a = cocks_pkg.extract("111111111111111111111111111111111111111111111111")
    assert gmpy2.jacobi(a, cocks_pkg.n) == 1
    pytest.raises(InvalidIdentityString, cocks_pkg.extract, "")
