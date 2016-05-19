from helper import Typename


class I(metaclass=Typename("I")):
    """
    the identity operator
    (lambda x: x)(5) => 5

    >>> I(5).b()
    5
    """
    def __init__(self, x):
        self.x = x

    def b(self):
        return self.x

    def __str__(self):
        return "(I " + str(self.x) + ")"

    def __repr__(self):
        return "<" + self.__str__() + ">"

    @classmethod
    def to_sk(cls):
        return S(K).dot(K)


class K(metaclass=Typename("K")):
    """
    which forms constant functions
    (lambda x, y)(True, False) => True

    >>> K(True).dot(False).b()
    True
    """
    is_class = True
    def __init__(self, x):
        self.x = x
        self.is_class = False

    @classmethod
    def d(self, x):
        return K(x)

    def dot(self, y):
        return K2(self.x, y)


    def __str__(self):
        return "(K " + str(self.x) + ")"

    def __repr__(self):
        return "<" + self.__str__() + ">"


class K2(metaclass=Typename("K")):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def b(self):
        return self.x

    def dot(self, z):
        x = self.b()
        try:
            if x.is_class:
                return x.d(z)
            else:
                return x.dot(z)
        except AttributeError:
            return x(z)

    def __repr__(self):
        return "<" + self.__str__() + ">"

    def __str__(self):
        return "(K " + str(self.x) + " " + str(self.y) + ")"


class S(metaclass=Typename("S")):
    """
    a stronger composition operator
    (lambda x, y, z)(f, g, h) => f(h, g(h))

    >>> S(K).dot(K).dot(5).b().b()
    5
    """

    is_class = True
    def __init__(self, x):
        self.x = x
        self.is_class = False

    @classmethod
    def d(cls, x):
        return S(x)

    def dot(self, y):
        return S2(self.x, y)

    def __str__(self):
        return "S " + str(self.x)

    def __repr__(self):
        return "<" + self.__str__() + ">"


class S2(metaclass=Typename("S")):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dot(self, z):
        return S3(self.x, self.y, z)

    def __str__(self):
        return "(S " + str(self.x) + " " + str(self.y) + ")"

    def __repr__(self):
        return "<" + self.__str__() + ">"


class S3(metaclass=Typename("S")):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __yz__(self):
        try:
            if self.y.is_class:
                return self.y.d(self.z)
            else:
                return self.y.dot(self.z)
        except AttributeError:
            return self.y(self.z)

    def b(self):
        xz = self.x.dot(self.z)
        return xz.dot(self.__yz__())

    def __str__(self):
        return "(S " + str(self.x) + " " + str(self.y) + " " + str(self.z) + ")"

    def __repr__(self):
        return "<" + self.__str__() + ">"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
