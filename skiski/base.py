from copy import copy


class CombinatorBase:

    @classmethod
    def is_weak(cls, x):
        return isinstance(x, type) or not hasattr(x, "__w__")

    def w(self):
        return self

    def __repr__(self):
        return "<" + self.__str__() + ">"


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

    def __w__(self, x):
        return self.dot(x)

    def w(self):
        new_stack = []
        for s in self.stack:
            if hasattr(s, "w"):
                new_stack.append(s.w())
        self.stack = new_stack
        return self
