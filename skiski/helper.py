def Typename(name):
    class TypeN(type):
        def __repr__(cls):
            return name
    return TypeN
