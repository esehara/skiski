from skiski.helper import Typename
from copy import copy


class VirtualCurry:

    def __b__(self, x):
        return self.dot(x)


class V:
    """
    generate variable obeject

    >>> I(V("x"))
    (I x)
    >>> V("x").dot(S).dot(K).dot(I)
    (x S K I)
    """

    def __init__(self, name):
        self.name = name
        self.stack = []

    def _str_stack_(self):
        return " ".join([str(x) for x in self.stack])

    def __str__(self):
        if len(self.stack) == 0:
            return str(self.name)
        else:
            return "(" + str(self.name) + " " + self._str_stack_() + ")"

    def __repr__(self):
        return self.__str__()

    def __copy__(self):
        new_v = V(self.name)
        new_v.stack = copy(self.stack)
        return new_v

    def dot(self, x):
        new_v = self.__copy__()
        new_v.stack.append(x)
        return new_v

    def __b__(self, x):
        return self.dot(x)

    def b(self):
        new_stack = []
        for s in self.stack:
            if hasattr(s, "b"):
                new_stack.append(s.b())
        self.stack = new_stack
        return self

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

    @classmethod
    def __b__(cls, x):
        if isinstance(cls, type):
            return cls(x)
        else:
            return cls.dot(x)

    def dot(self, x):
        y = self.b()
        return y.__b__(x)

    def __str__(self):
        return "(I " + str(self.x) + ") "

    def __repr__(self):
        return self.__str__()

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
    def __init__(self, x):
        self.x = x

    def dot(self, y):
        return K2(self.x, y)

    def __str__(self):
        return "(K " + str(self.x) + ") "

    def __repr__(self):
        return self.__str__()


class K2(metaclass=Typename("K")):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def b(self):
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

    >>> S(K).dot(K).dot(5).b().b()
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

    def b(self):
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

    def b(self):
        return self

    def __repr__(self):
        return self.__str__()


class S3(metaclass=Typename("S")):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def b(self):
        yz = self.__b__(self.y, self.z)
        if hasattr(yz, "b"):
            yz = yz.b()

        xz = self.__b__(self.x, self.z)
        if hasattr(xz, "b"):
            xz = xz.b()

        if isinstance(xz, type):
            return xz(yz)
        else:
            return xz.dot(yz)

    def __str__(self):
        return "(S " + str(self.x) + " " + str(self.y) + " " + str(self.z) + ") "

    def __repr__(self):
        return self.__str__()

    def _eval_i_(self, x):
        while isinstance(x, I):
            x = x.b()
        return x

    def __b__(self, x, y):
        x = self._eval_i_(x)
        y = self._eval_i_(y)

        try:
            if isinstance(x, type):
                return x(y)
            else:
                return x.dot(y)
        except AttributeError:
            return x(z)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
