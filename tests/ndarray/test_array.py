from parachute import Array


def test_array_ndim_0():
    a = Array(ndim=0)
    assert a.is_valid(1)
    assert not a.is_valid([1, 2])
    assert not a.is_valid([[1, 2], [3, 4]])
    assert not a.is_valid([[[1, 2], [3, 4]]])


def test_array_ndim_1():
    a = Array(ndim=1)
    assert not a.is_valid(1)
    assert a.is_valid([1, 2])
    assert not a.is_valid([[1, 2], [3, 4]])
    assert not a.is_valid([[[1, 2], [3, 4]]])


def test_array_ndim_2():
    a = Array(ndim=2)
    assert not a.is_valid(1)
    assert not a.is_valid([1, 2])
    assert a.is_valid([[1, 2], [3, 4]])
    assert not a.is_valid([[[1, 2], [3, 4]]])
