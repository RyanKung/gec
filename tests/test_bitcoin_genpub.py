from bitcoin import decode_privkey, fast_multiply, get_privkey_format
from hashlib import sha256
import random
import base58
from gec.groups import EllipticCurveGroup, CyclicGroup
from gec.fields import FiniteField

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
key = random.randint(1, N)


def gen_pri_key(key, version=128, compress=1):
    private_key = bytes([version]) + key.to_bytes(
        32, byteorder='big') + bytes([compress])
    auth = sha256(sha256(private_key).digest()).digest()[:4]
    res = private_key + auth
    assert len(res) == 1 + 32 + 1 + 4
    return base58.b58encode(res)


pri_key = gen_pri_key(key)


class FiniteFieldBTC(FiniteField):
    P = 2**256 - 2**32 - 977


class EllipticCurveGroupBTC(EllipticCurveGroup):
    A = 0
    B = 7


G = EllipticCurveGroupBTC((FiniteFieldBTC(Gx), FiniteFieldBTC(Gy)))


class EllipticCurveCyclicSubgroupBTC(CyclicGroup):
    G = G
    N = N


def test_verify_pri_key():
    assert get_privkey_format(pri_key) == 'wif_compressed'
    assert decode_privkey(pri_key, 'wif_compressed') == key


def test_calcu_pub_key():
    res = G @ EllipticCurveCyclicSubgroupBTC(key)
    ans = fast_multiply((Gx, Gy), key)
    assert (res.value[0].value, res.value[1].value) == ans
