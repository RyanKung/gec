from gec.algorithm import schoof_algorithm


def test_schoof():
    assert schoof_algorithm(23, 4, 2) == 21
