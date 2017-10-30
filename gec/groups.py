from abc import abstractproperty
from .abstract import Group


class EllipticCurveGroup(Group):
    # for y^2 = x^3 + A * x + B
    A = abstractproperty()
    B = abstractproperty()

    def op(self, g):
        if g.value == 0:
            return self
        field = self.value[0].__class__

        if self.value[0] != g.value[0]:
            m = (self.value[1] - g.value[1]) / (self.value[0] - g.value[0])
        if self.value[0] == g.value[0]:
            m = (field(3) * self.value[0] * self.value[0] +
                 field(self.A)) / (field(2) * self.value[1])
        r_x = (m * m - self.value[0] - g.value[0])
        r_y = (self.value[1] + m * (r_x - self.value[0]))
        return self.__class__((r_x, -r_y))

    def inverse(self):
        return self.__class__((self.value[0], -self.value[0]))

    @property
    def identity(self):
        # The abstract zero of EC Group
        return self.__class__(0)


class CyclicGroup(Group):
    '''
    With Lagrange's therem
    the order of a subgroup is a divisor of the order of the parent group
    '''
    # The Base Point
    G = abstractproperty()
    # Order of subgroup
    N = abstractproperty()

    def op(self, g):
        '''
        2 + 3 -> 2G + 3G -> 5G
        '''
        if g.value == 0:
            return self
        return self.__class__((self.value + g.value) % self.N)

    def inverse(self):
        return self.__class__(self.N - 1 - self.value)

    @property
    def identity(self):
        return self.__class__(0)
