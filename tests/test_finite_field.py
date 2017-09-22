from gec.fields import FiniteField


class SomeFiniteField(FiniteField):
    P = 19


def test_finite_field():
    a = SomeFiniteField(2)
    b = SomeFiniteField(3)
    assert (a + b) == SomeFiniteField(5)
    assert (a * b) == SomeFiniteField(6)
    assert (a - b) == SomeFiniteField(18)
    assert (a / b) == SomeFiniteField(7)
    assert -a == SomeFiniteField(17)
    assert ~a == SomeFiniteField(10)
