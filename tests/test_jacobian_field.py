from gec.fields import FiniteField
from gec.groups import JacobianGroup
from bitcoin import jacobian_add, jacobian_double, jacobian_multiply

A = 0
B = 7
P = 2**256 - 2**32 - 977
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337


class FiniteFieldBTC(FiniteField):
    P = P


class JacobianGroupBTC(JacobianGroup):
    N = N
    A = A


def test_jacobian_double():
    j = JacobianGroupBTC(
        (
            FiniteFieldBTC(5),
            FiniteFieldBTC(8),
            FiniteFieldBTC(1)
        )
    )
    ans = jacobian_double((5, 8, 1))
    ret = j.double()

    assert (
        ret.value[0].value,
        ret.value[1].value,
        ret.value[2].value
    ) == ans


def test_jacobian_add():
    j = JacobianGroupBTC(
        (
            FiniteFieldBTC(5),
            FiniteFieldBTC(8),
            FiniteFieldBTC(1)
        )
    )
    k = JacobianGroupBTC(
        (
            FiniteFieldBTC(3),
            FiniteFieldBTC(22),
            FiniteFieldBTC(1)
        )
    )
    ans = jacobian_add((5, 8, 1), (3, 22, 1))
    ret = j + k
    assert (
        ret.value[0].value,
        ret.value[1].value,
        ret.value[2].value
    ) == ans


def test_jacobian_multi():
    jg = JacobianGroupBTC(
        (
            FiniteFieldBTC(5),
            FiniteFieldBTC(8),
            FiniteFieldBTC(1)
        )
    )
    ans = jacobian_multiply((5, 8, 1), 2)
    ret = jg @ 2
    assert (
        ret.value[0].value,
        ret.value[1].value,
        ret.value[2].value
    ) == ans

    ans = jacobian_multiply((5, 8, 1), 3)
    ret = jg @ 3
    assert (
        ret.value[0].value,
        ret.value[1].value,
        ret.value[2].value
    ) == ans
