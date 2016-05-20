from skiski.base import CombinatorBase
from skiski.helper import Typename
from skiski.ski import S, K, I


class B(metaclass=Typename("B")):
    """
    which composes two function

    >>> B(lambda x: x).dot(lambda x: x + 5).dot(5).w()
    10
    >>> S(B).dot(I).dot(V("Succ")).w().w().dot("Zero").w()
    (Succ (Succ Zero))
    """

    def __init__(self, x):
        self.x = x
        self.is_class = False

    def dot(self, y):
        return _B2(self.x, y)

    def __str__(self):
        return "(B " + str(self.x) + ") "

    def __repr__(self):
        return self.__str__()

    def w(self):
        return self

    @classmethod
    def to_ski(cls):
        """
        S(KS)K Combinator is virtually B Combinator:

        >>> B.to_ski()
        (S (K S)  K) 
        >>> sksk = S(B.to_ski()).dot(I).dot(V("Succ")).w().dot(V("Zero"))
        (Succ (Succ Zero))
        """
        return S(K(S)).dot(K)


class _B2(CombinatorBase, metaclass=Typename("B")):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dot(self, z):
        return _B3(self.x, self.y, z)

    def __str__(self):
        return "(B " + str(self.x) + " " + str(self.y) + ") "

    def w(self):
        if self.is_weak(self.y):
            self.y = self.y.w()
        return self


class _B3(CombinatorBase, metaclass=Typename("B")):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.is_class = False

    def w(self):
        yz = self.__w__(self.y, self.z)
        xyz = self.__w__(self.x, yz)
        return xyz

    def __w__(self, x, y):
        if self.is_weak(x):
            return x(y)
        else:
            return x.__w__(y)

    def __str__(self):
        return "(B " + str(self.x) + " " + str(self.y) + " " + str(self.z) + ") "

    def __repr__(self):
        return "<" + self.__str__() + ">"


class R(CombinatorBase, metaclass=Typename("R")):

    def __init__(self, x):
        self.x = x

    def dot(self, y):
        return _R2(self.x, y)

    def __str__(self):
        return "(R " + str(self.x) + ") "


class _R2(CombinatorBase, metaclass=Typename("R")):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dot(self, z):
        return _R3(self.x, self.y, z)

    def __w__(self, x, y):
        if self.is_weak(x):
            return x(y)
        else:
            return x.__w__(y)

    def w(self):
        return self.__w__(self.y, self.x)

    def __str__(self):
        return "(R" + str(self.x) + " " + str(self.y) + ")"

    @classmethod
    def to_ski(cls):
        return S(K(S(I))).dot(K)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
