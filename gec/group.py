from abc import ABCMeta, abstractmethod, abstractproperty


class Groupoid(metaclass=ABCMeta):
    def __init__(self, v):
        self.value = v

    @abstractmethod
    def addop(self, g: 'Group') -> 'Group':
        pass

    def __add__(self, g: 'Group') -> 'Group':
        '''
        Allowing call associativity operator via A@B
        Strict limit arg `g` and ret `res` should be subtype of Group,
        For obeying axiom `closure` (1)
        '''
        assert isinstance(g, type(self))
        res = self.addop(g)
        assert isinstance(res, type(self))
        return res

    def __repr__(self):
        return "%s::%s" % (
            type(self).__name__,
            self.value
        )

    def __str__(self):
        return str(self.value)


class SemiGroup(Groupoid, metaclass=ABCMeta):
    @abstractmethod
    def addop(self, g: 'Group') -> 'Group':
        '''
        The Operator for obeying axiom `associativity` (2)
        '''
        pass


class Monoid(SemiGroup, metaclass=ABCMeta):

    @abstractproperty
    def zero(self):
        '''
        The value for obeying axiom `identity` (3)
        '''
        pass


class Group(Monoid, metaclass=ABCMeta):

    @abstractmethod
    def addop_inverse(self, g: 'Group') -> 'Group':
        '''
        Implement for axiom `inverse`
        '''
        pass

    def __sub__(self, g: 'Group') -> 'Group':
        return self.__add__(self.addop_inverse(g))

    def __neg__(self, g: 'Group') -> 'Group':
        return self.addop_inverse(g)


class Field(Group, metaclass=ABCMeta):

    @abstractmethod
    def mulop(self, g: 'Group') -> 'Group':
        '''
        The Operator for obeying axiom `associativity` (2)
        '''
        pass

    @abstractmethod
    def mulop_inverse(self, g: 'Group') -> 'Group':
        '''
        Implement for axiom `inverse`
        '''
        pass

    def __mul__(self, g: 'Group') -> 'Group':
        '''
        Allowing call associativity operator via A@B
        Strict limit arg `g` and ret `res` should be subtype of Group,
        For obeying axiom `closure` (1)
        '''
        res = self.mulop(g)
        assert isinstance(res, type(self))
        return res

    def __div__(self, g: 'Group') -> 'Group':
        return self.__add__(self.mul_inverse(g))
