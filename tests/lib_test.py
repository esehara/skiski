import pytest
from skiski.ski import S, K, I
from skiski.lib import B, R


def test_composite_function():
    a = lambda x: x * 5
    b = lambda x: x - 3
    assert B(a).dot(b).dot(5).w() == 10


def test_sksk_is_b():
    a = lambda x: x * 5
    b = lambda x: x - 3
    b_comb = B(a).dot(b).dot(5).w()
    sksk = B.to_ski().dot(a).w().dot(b).dot(5).w()
    assert b_comb == sksk


def test_reverse_composite_function():
    a = lambda x: x * 5
    assert R(5).dot(a).w() == 25


def test_sksik_is_r():
    a = lambda x: x * 5
    r_comb = R(5).dot(a).w()
    sksik = S(K(S(I))).dot(K).dot(5).w().dot(a).w()
    assert r_comb == sksik
