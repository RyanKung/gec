from gec.groups import EllipicCurveGroup
from gec.fields import FiniteField


class SomeEllipicCurveGroup(EllipicCurveGroup):
    A = -7
    B = 10


class FiniteField97(FiniteField):
    P = 97


def test_simple_ec():
    a = SomeEllipicCurveGroup((1, 2))
    b = SomeEllipicCurveGroup((3, 4))
    assert (a + b) == SomeEllipicCurveGroup((-3, 2))

    a = SomeEllipicCurveGroup((1, 2))
    b = SomeEllipicCurveGroup((1, 2))
    assert (a + b) == SomeEllipicCurveGroup((-1, -4))

    a = SomeEllipicCurveGroup((2, 2))
    b = SomeEllipicCurveGroup((1, 2))
    assert (a + b) == SomeEllipicCurveGroup((-3, -2))

    a = SomeEllipicCurveGroup((1, 2))
    assert a + a == a @ 2

    a = SomeEllipicCurveGroup((1, 2))
    assert a + a + a == a @ 3


def test_ec_over_ff():
    a = SomeEllipicCurveGroup((FiniteField97(11), (FiniteField97(10))))
    b = SomeEllipicCurveGroup((FiniteField97(87), (FiniteField97(27))))
    res = SomeEllipicCurveGroup((FiniteField97(74), (FiniteField97(41))))
    assert (a + b) == res
    assert a @ 2 == a + a
