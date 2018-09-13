import pytest

# from parachute import Shape

pytestmark = pytest.mark.skip


def test_shapespec_any():
    s = Shape(None)
    assert not s.is_valid("not a shapespec")
    assert not s.is_valid((4, "4"))
    assert not s.is_valid((4, None))
    assert not s.is_valid((None,))
    assert s.is_valid(())
    assert s.is_valid((4,))
    assert s.is_valid((5, 4))
    assert s.is_valid((5, 0))
    assert s.is_valid((5, False))
    assert s.is_valid((5, 42098507180))
    assert s.is_valid((5, 4, 0, 9))


def test_shapespec_fix():
    s = Shape((5, 4))
    assert not s.is_valid("not a shapespec")
    assert not s.is_valid((4, "4"))
    assert not s.is_valid((4, None))
    assert not s.is_valid((None,))
    assert not s.is_valid(())
    assert not s.is_valid((4,))
    assert s.is_valid((5, 4))
    assert not s.is_valid((5, 0))
    assert not s.is_valid((5, False))
    assert not s.is_valid((5, 42098507180))
    assert not s.is_valid((5, 4, 0, 9))


def test_shapespec_wildcard():
    s = Shape((5, None))
    assert not s.is_valid("not a shapespec")
    assert not s.is_valid((4, "4"))
    assert not s.is_valid((4, None))
    assert not s.is_valid((None,))
    assert not s.is_valid(())
    assert not s.is_valid((4,))
    assert s.is_valid((5, 4))
    assert s.is_valid((5, 0))
    assert s.is_valid((5, False))
    assert s.is_valid((5, 42098507180))
    assert not s.is_valid((5, 4, 0, 9))
