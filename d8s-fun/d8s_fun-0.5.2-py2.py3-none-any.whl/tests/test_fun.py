import time

from d8s_fun import password_create, spin_until_done


def test_password_create_1():
    assert len(password_create()) == 15
    assert len(password_create(length=20)) == 20

    new_pwd = password_create(length=21, character_set='ab')
    assert len(new_pwd) == 21
    new_pwd_has_only_a_b = new_pwd.count('a') + new_pwd.count('b') == 21
    assert new_pwd_has_only_a_b


@spin_until_done
def spin_until_done_test_func_a(a):
    """."""
    time.sleep(1)
    return a


def test_spin_until_done_1():
    import timeit

    time_duration = timeit.timeit('spin_until_done_test_func_a(1)', number=3, globals=globals())
    assert 1 < time_duration > 2
