from ski import S, K, I
from helper import Typename


class B(metaclass=Typename("B")):
    """
    which composes two function

    >>> B(lambda x: x).dot(lambda x: x + 5).dot(5).b()
    10
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

    @classmethod
    def to_ski(cls):
        return S(K(S)).dot(K)


class B2(metaclass=Typename("B")):

    is_class = True
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_class = False

    def dot(self, z):
        return B3(self.x, self.y, z)

    def __str__(self):
        return "(B " + str(self.x) + " " + str(self.y) + ") "

    def __repr__(self):
        return "<" + self.__str__() + ">"


class B3(metaclass=Typename("B")):

    is_class = True
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.is_class = False

    def b(self):
        return self.x(self.y(self.z))

    def __str__(self):
        return "(B " + str(self.x) + " " + str(self.y) + str(self.z) + ") "

    def __repr__(self):
        return "<" + self.__str__() + ">"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
