class UndefinedName:
    def __str__(self):
        return 'Undefined name'

    def __repr__(self):
        return self.__str__()


UNDEFINED = UndefinedName()
