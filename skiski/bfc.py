from ski import S, K, I, V
from helper import Typename


class B(metaclass=Typename("B")):
    """
    which composes two function

    >>> B(lambda x: x).dot(lambda x: x + 5).dot(5).b()
    10
    >>> S(B).dot(I).dot(V("Succ")).b().b().dot("Zero").b()
    (Succ (Succ Zero))
    """
    is_class = True
    def __init__(self, x):
        self.x = x
        self.is_class = False

    def dot(self, y):
        return B2(self.x, y)

    def __str__(self):
        return "(B " + str(self.x) + ") "

    def __repr__(self):
        return self.__str__()

    def b(self):
        return self

    @classmethod
    def to_ski(cls):
        return S(K(S)).dot(K)


class B2(metaclass=Typename("B")):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_class = False

    def dot(self, z):
        return B3(self.x, self.y, z)

    def __str__(self):
        return "(B " + str(self.x) + " " + str(self.y) + ") "

    def b(self):
        self.y = self.y.b()
        return self

    def __repr__(self):
        return "<" + self.__str__() + ">"


class B3(metaclass=Typename("B")):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.is_class = False

    def b(self):
        yz = self.__b__(self.y, self.z)
        xyz = self.__b__(self.x, yz)
        return xyz

    def __b__(self, x, y):
        if isinstance(x, type) or not hasattr(x, "__b__"):
            return x(y)
        else:
            return x.__b__(y)

    def __str__(self):
        return "(B " + str(self.x) + " " + str(self.y) + " " + str(self.z) + ") "

    def __repr__(self):
        return "<" + self.__str__() + ">"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
