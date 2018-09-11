from typing import Any
from parachute import Spec


def test_any():
    other = Spec(Any)
    assert other.conforms("jo")
    assert other.conforms(True)
    assert other.conforms([5, "je"])
    assert other.conforms(Spec)
    broad = Spec()
    assert broad.conforms("jo")
    assert broad.conforms(True)
    assert broad.conforms([5, "je"])
    assert broad.conforms(Spec)


def test_float():
    s = Spec(float)
    assert s.conforms(4)
    assert s.conforms(5.3)
    assert s.conforms(False)
    assert not s.conforms("y")
    assert not s.conforms([4, 5.3])
    assert not s.conforms([5.3])
