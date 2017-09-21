from abc import abstractproperty
from .group import Field, Group


class FiniteField(Field):
    P = abstractproperty()

    def _eulidean_alg(self, g, n):
        '''
        Extended Euclidean Algorithm
        '''
        if g == 0:
            return 0
        lm, hm = 1, 0
        low, high = g % n, n
        while low > 1:
            r = high // low
            nm, new = hm - lm * r, high - low * r
            lm, low, hm, high = nm, new, lm, low
        return lm % n

    def zero(self):
        return 0

    def addop_inverse(self):
        return self.__class__(-self.value)

    def mulop_inverse(self):
        return self.__class__(self._eulidean_alg(self.value, self.P))

    def mulop(self, n):
        return self.__class__((self.value * n.value) % self.P)

    def addop(self, n):
        return self.__class__((self.value + n.value) % self.P)


class ECGroup(Group):

    # Elliptic curve parameters (secp256k1)
    # The prime pp that specifies the size of the finite field.
    P = abstractproperty()
    # The order nn of the subgrouop.
    N = abstractproperty()
    # The coefficients aa and bb of the elliptic curve equation.
    A = abstractproperty()
    B = abstractproperty()

    def _eulidean_alg(self, g, n):
        '''
        Extended Euclidean Algorithm
        '''
        if g == 0:
            return 0
        lm, hm = 1, 0
        low, high = g % n, n
        while low > 1:
            r = high // low
            nm, new = hm - lm * r, high - low * r
            lm, low, hm, high = nm, new, lm, low
        return lm % n

    def _to_jacobian(self, p):
        o = (p[0], p[1], 1)
        return o

    def _from_jacobian(self, p):
        z = self._eulidean_alg(p[2], self.P)
        return ((p[0] * z**2) % self.P, (p[1] * z**3) % self.P)

    def _jacobian_double(self, p):
        if not p[1]:
            return (0, 0, 0)
        ysq = (p[1] ** 2) % self.P
        S = (4 * p[0] * ysq) % self.P
        M = (3 * p[0] ** 2 + self.A * p[2] ** 4) % self.P
        nx = (M**2 - 2 * S) % self.P
        ny = (M * (S - nx) - 8 * ysq ** 2) % self.P
        nz = (2 * p[1] * p[2]) % self.P
        return (nx, ny, nz)

    def _jacobian_add(self, p, q):
        if not p[1]:
            return q
        if not q[1]:
            return p
        U1 = (p[0] * q[2] ** 2) % self.P
        U2 = (q[0] * p[2] ** 2) % self.P
        S1 = (p[1] * q[2] ** 3) % self.P
        S2 = (q[1] * p[2] ** 3) % self.P
        if U1 == U2:
            if S1 != S2:
                return (0, 0, 1)
            return self._jacobian_double(p)

        H = U2 - U1
        R = S2 - S1
        H2 = (H * H) % self.P
        H3 = (H * H2) % self.P
        U1H2 = (U1 * H2) % self.P
        nx = (R ** 2 - H3 - 2 * U1H2) % self.P
        ny = (R * (U1H2 - nx) - S1 * H3) % self.P
        nz = (H * p[2] * q[2]) % self.P
        return (nx, ny, nz)

    def _jacobian_multiply(self, a, n):
        if a[1] == 0 or n == 0:
            return (0, 0, 1)
        if n == 1:
            return a
        if n < 0 or n >= self.N:
            return self._jacobian_multiply(a, n % self.N)
        if (n % 2) == 0:
            return self._jacobian_double(self._jacobian_multiply(a, n // 2))
        if (n % 2) == 1:
            return self._jacobian_add(self._jacobian_double(self._jacobian_multiply(a, n // 2)), a)

    @property
    def zero(self):
        return self.__class__((0, 0))

    def addop_inverse(self):
        return self.__class__((-self.value[0], -self.value[1]))

    def mulop_inverse(self):
        return self.__class__(self._eulidean_alg(self.value, self.P))

    def mulop(self, n):
        return self.__class__(
            self._from_jacobian(
                self._jacobian_multiply(
                    self._to_jacobian(self.value), n
                )
            )
        )

    def addop(self, n):
        return self.__class__(
            self._from_jacobian(
                self._jacobian_add(
                    self._to_jacobian(self.value),
                    self._to_jacobian(n.value)
                )
            )
        )
