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
    a = lambda x: x
    assert S(K).dot(K).dot(10).w().w() == 10
