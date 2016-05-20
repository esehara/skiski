from skiski.base import V
from skiski.helper import Typename
from copy import copy


class VirtualCurry:

    def __b__(self, x):
        return self.dot(x)


class I(metaclass=Typename("I")):
    """
    the identity operator
    (lambda x: x)(5) => 5

    >>> I(5).w()
    5
    """
    def __init__(self, x):
        self.x = x

    def w(self):
        return self.x

    @classmethod
    def __w__(cls, x):
        if isinstance(cls, type):
            return cls(x)
        else:
            return cls.dot(x)

    def dot(self, x):
        y = self.w()
        return y.__w__(x)

    def __str__(self):
        return "(I " + str(self.x) + ") "

    def __repr__(self):
        return self.__str__()

    @classmethod
    def to_ski(cls):
        """
        Only S and K combinator make I combinator.

        >>> skk = S(K).dot(K).dot(1)
        >>> skk.w()
        (K 1 (K 1) )
        >>> skk.w().w()
        1

        It's behavior means 'I combinator'.
        """
        return S(K).dot(K)


class K(metaclass=Typename("K")):
    """
    which forms constant functions
    (lambda x, y)(True, False) => True

    >>> K(True).dot(False).w()
    True
    """
    def __init__(self, x):
        self.x = x

    def dot(self, y):
        return _K2(self.x, y)

    def __str__(self):
        return "(K " + str(self.x) + ") "

    def __repr__(self):
        return self.__str__()


class _K2(metaclass=Typename("K")):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def w(self):
        return self.x

    def dot(self, z):
        x = self.b()
        if isinstance(x, type):
            return x(z)
        else:
            return x.dot(z)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "(K " + str(self.x) + " " + str(self.y) + ") "


class S(metaclass=Typename("S")):
    """
    a stronger composition operator
    (lambda x, y, z)(f, g, h) => f(h, g(h))

    >>> S(K).dot(K).dot(5).w().w()
    5

    SII(SII) combinator is infinity loop ;)

    >>> siisii = S(I).dot(I).dot(S(I).dot(I))
    >>> siisii.b().b().b().b()
    (S I I (I (S I I) ) ) 
    """

    def __init__(self, x):
        self.x = x

    def dot(self, y):
        return S2(self.x, y)

    def w(self):
        return self

    def __str__(self):
        return "(S " + str(self.x) + ") "

    def __repr__(self):
        return self.__str__()


class S2(VirtualCurry, metaclass=Typename("S")):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dot(self, z):
        return S3(self.x, self.y, z)

    def __str__(self):
        return "(S " + str(self.x) + " " + str(self.y) + ") "

    def w(self):
        return self

    def __repr__(self):
        return self.__str__()


class S3(metaclass=Typename("S")):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def w(self):
        yz = self._wrap_w_(self.y, self.z)
        xz = self._wrap_w_(self.x, self.z)

        if self.is_dot(xz):
            return xz.dot(yz)
        else:
            return xz(yz)

    def __str__(self):
        return "(S " + str(self.x) + " " + str(self.y) + " " + str(self.z) + ") "

    def __repr__(self):
        return self.__str__()

    @classmethod
    def is_dot(cls, x):
        return (not isinstance(x, type)) and hasattr(x, "dot")

    @classmethod
    def _wrap_w_(cls, x, y):
        xy = cls.__w__(x, y)
        if hasattr(xy, "w"):
            xy = xy.w()
        return xy

    @classmethod
    def _eval_i_(cls, x):
        while isinstance(x, I):
            x = x.w()
        return x

    @classmethod
    def __w__(cls, x, y):
        x = cls._eval_i_(x)
        y = cls._eval_i_(y)

        if cls.is_dot(x):
            return x.dot(y)
        else:
            return x(y)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
