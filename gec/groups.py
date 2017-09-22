from abc import abstractproperty
from .abstract import Group, AbstractIdentity


class EllipicCurveGroup(Group):
    # for y^2 = x^3 + A * x + B
    A = abstractproperty()
    B = abstractproperty()

    def op(self, g):
        if isinstance(g.value, AbstractIdentity):
            return self
        field = self.value[0].__class__

        if self.value[0] != g.value[0]:
            m = (self.value[1] - g.value[1]) / (self.value[0] - g.value[0])
        if self.value[0] == g.value[0]:
            m = (field(3) * self.value[0] * self.value[0] + field(self.A)) / (field(2) * self.value[1])
        r_x = (m * m - self.value[0] - g.value[0])
        r_y = (self.value[1] + m * (r_x - self.value[0]))
        return self.__class__((r_x, -r_y))

    def inverse(self):
        return self.__class__((self.value[0], -self.value[0]))

    @property
    def identity(self):
        return self.__class__(AbstractIdentity())
