from gec.groups import EllipticCurveGroup, CyclicGroup
from gec.fields import FiniteField


class EllipticCurveGroupN710(EllipticCurveGroup):
    A = -7
    B = 10


class EllipticCurveGroup0203(EllipticCurveGroup):
    A = 2
    B = 3


class FiniteField97(FiniteField):
    P = 97


class EllipticCurveCyclicSubgroup36(CyclicGroup):
    G = EllipticCurveGroupN710((FiniteField97(3), FiniteField97(6)))
    N = 5


def test_simple_ec():
    a = EllipticCurveGroupN710((1, 2))
    b = EllipticCurveGroupN710((3, 4))
    assert (a + b) == EllipticCurveGroupN710((-3, 2))

    a = EllipticCurveGroupN710((1, 2))
    b = EllipticCurveGroupN710((1, 2))
    assert (a + b) == EllipticCurveGroupN710((-1, -4))

    a = EllipticCurveGroupN710((2, 2))
    b = EllipticCurveGroupN710((1, 2))
    assert (a + b) == EllipticCurveGroupN710((-3, -2))

    a = EllipticCurveGroupN710((1, 2))
    assert a + a == a @ 2

    a = EllipticCurveGroupN710((1, 2))
    assert a + a + a == a @ 3


def test_ec_over_ff():
    a = EllipticCurveGroupN710((FiniteField97(11), (FiniteField97(10))))
    b = EllipticCurveGroupN710((FiniteField97(87), (FiniteField97(27))))
    res = EllipticCurveGroupN710((FiniteField97(74), (FiniteField97(41))))
    assert (a + b) == res
    assert a @ 7 == a + a + a + a + a + a + a


def test_cyclic_subgroup():
    a = EllipticCurveCyclicSubgroup36(1)
    b = EllipticCurveCyclicSubgroup36(2)
    assert a + b == EllipticCurveCyclicSubgroup36(3)

    assert EllipticCurveGroup0203(
        (FiniteField97(3), FiniteField97(6))
    ) @ (a + b) == EllipticCurveGroup0203(
        (FiniteField97(80), FiniteField97(87))
    )
    a = EllipticCurveCyclicSubgroup36(1)
    b = EllipticCurveCyclicSubgroup36(6)

    assert EllipticCurveGroup0203(
        (FiniteField97(3), FiniteField97(6))
    ) @ (a + b) == EllipticCurveGroup0203(
        (FiniteField97(80), FiniteField97(10))
    )

    a = EllipticCurveCyclicSubgroup36(1)
    b = EllipticCurveCyclicSubgroup36(9)

    assert EllipticCurveGroup0203(
        (FiniteField97(3), FiniteField97(6))
    ) @ (a + b) == EllipticCurveGroup0203(0)
