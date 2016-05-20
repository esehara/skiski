import pytest
from skiski.ski import S, K, I, V


def test_identity_operator():
    assert I(1).w() == 1


def test_identity_skk():
    skk = S(K).dot(K).dot(1)
    i = I(1)
    assert skk.w().w() == i.w()


def test_const_function():
    assert K(10).dot(20).w() == 10


def test_share_function():
    a = lambda x: x * 5
    b = lambda x: x - 3
    assert S(a).dot(b).dot(5).w() == 10
