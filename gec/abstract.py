from abc import ABCMeta, abstractmethod, abstractproperty
from .algorithm import double_and_add_algorithm


class Groupoid(metaclass=ABCMeta):

    __slot__ = ''

    def __init__(self, v):
        self.value = v

    @abstractmethod
    def op(self, g: 'Group') -> 'Group':
        pass

    def __eq__(self, b) -> bool:
        return self.value == b.value

    def __add__(self, g: 'Group') -> 'Group':
        '''
        Allowing call associativity operator via A + B
        Strict limit arg `g` and ret `res` should be subtype of Group,
        For obeying axiom `closure` (1)
        '''
        assert isinstance(g, type(self))
        res = self.op(g)
        assert isinstance(res, type(self))
        return res

    def __repr__(self):
        return "%s::%s" % (
            type(self).__name__,
            self.value
        )

    def __str__(self):
        return str(self.value)


class SemiGroup(Groupoid):
    @abstractmethod
    def op(self, g: 'Group') -> 'Group':
        '''
        The Operator for obeying axiom `associativity` (2)
        '''
        pass


class Monoid(SemiGroup):

    @abstractproperty
    def identity(self):
        '''
        The value for obeying axiom `identity` (3)
        '''
        pass

    def __matmul__(self, n):
        return double_and_add_algorithm(
            getattr(n, 'value', n), self, self.identity)


class Group(Monoid):

    @abstractmethod
    def inverse(self, g: 'Group') -> 'Group':
        '''
        Implement for axiom `inverse`
        '''
        pass

    def __sub__(self, g: 'Group') -> 'Group':
        '''
        Allow to reverse op via a - b
        '''
        return self.op(g.inverse())

    def __neg__(self) -> 'Group':
        return self.inverse()


class Field(Group):

    @abstractmethod
    def sec_op(self, g: 'Group') -> 'Group':
        '''
        The Operator for obeying axiom `associativity` (2)
        '''
        pass

    @abstractmethod
    def sec_inverse(self) -> 'Group':
        '''
        Implement for axiom `inverse`
        '''
        pass

    @abstractmethod
    def sec_identity(self):
        pass

    def __invert__(self):
        return self.sec_inverse()

    def __mul__(self, g: 'Group') -> 'Group':
        '''
        Allowing call associativity operator via A * B
        Strict limit arg `g` and ret `res` should be subtype of Group,
        For obeying axiom `closure` (1)
        '''
        res = self.sec_op(g)
        assert isinstance(res, type(self)), 'result shuould be %s' % type(self)
        return res

    def __truediv__(self, g: 'Group') -> 'Group':
        return self.sec_op(g.sec_inverse())
