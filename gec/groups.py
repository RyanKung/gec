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


class JacobianGroup(Group):
    A = abstractproperty()
    N = abstractproperty()

    def to_ecg(self, n=None):
        if not n:
            n = self
        z = ~(n.value[2])
        return (n.value[0] * z ** 2), n[1] * z ** 3

    def double(self, n=None):
        if not n:
            n = self
        field = n.value[0].__class__
        if not n.value[1].value:
            return n.__class__(
                (
                    field(0),
                    field(0),
                    field(0)
                )
            )

        ysq = self.value[1] ** 2
        S = self.value[0] @ 4 * ysq
        M = (self.value[0] ** 2) @ 3 + (self.value[2] ** 4) @ self.A
        nx = M ** 2 - S @ 2
        ny = M * (S - nx) - (ysq ** 2) @ 8
        nz = field(2) * self.value[1] * self.value[2]
        return self.__class__((nx, ny, nz))

    @property
    def identity(self):
        field = self.value[0].__class__
        return self.__class__((field(0), field(0), field(0)))

    def inverse(self):
        pass

    def op(self, g):
        field = self.value[0].__class__
        if not self.value[1]:
            return g
        if not g.value[1]:
            return self
        U1 = self.value[0] * g.value[2] ** 2
        U2 = g.value[0] * self.value[2] ** 2
        S1 = self.value[1] * g.value[2] ** 3
        S2 = g.value[1] * self.value[2] ** 3
        if U1 == U2:
            if S1 != S2:
                return self.__class__(
                    (
                        field(0),
                        field(0),
                        field(1)
                    )
                )
            return self.double()
        H = field(U2.value - U1.value)
        R = field(S2.value - S1.value)
        H2 = H * H
        H3 = H * H2
        U1H2 = U1 * H2
        nx = (R ** 2) - H3 - (U1H2 @ 2)

        ny = R * (U1H2 - nx) - S1 * H3
        nz = H * self.value[2] * g.value[2]
        return self.__class__((nx, ny, nz))

    def __matmul__(self, n):
        field = self.value[0].__class__
        if self.value[1].value == 0 or n == 0:
            return self.__class__(
                (field(0), field(0), field(1))
            )
        if n == 1:
            return self
        if n < 0 or n >= self.N:
            return self @ (n % self.N)
        if (n % 2) == 0:
            return self.double(self @ (n // 2))
        if (n % 2) == 1:
            return self.double(self @ (n // 2)) + self
