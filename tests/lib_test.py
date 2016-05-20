import pytest
from skiski.lib import B


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
