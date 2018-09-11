from parachute import Shape


def test_shapespec_any():
    s = Shape(None)
    assert not s.validate("not a shapespec")
    assert not s.validate((4, "4"))
    assert not s.validate((4, None))
    assert not s.validate((None,))
    assert s.validate(())
    assert s.validate((4,))
    assert s.validate((5, 4))
    assert s.validate((5, 0))
    assert s.validate((5, False))
    assert s.validate((5, 42098507180))
    assert s.validate((5, 4, 0, 9))


def test_shapespec_fix():
    s = Shape((5, 4))
    assert not s.validate("not a shapespec")
    assert not s.validate((4, "4"))
    assert not s.validate((4, None))
    assert not s.validate((None,))
    assert not s.validate(())
    assert not s.validate((4,))
    assert s.validate((5, 4))
    assert not s.validate((5, 0))
    assert not s.validate((5, False))
    assert not s.validate((5, 42098507180))
    assert not s.validate((5, 4, 0, 9))


def test_shapespec_wildcard():
    s = Shape((5, None))
    assert not s.validate("not a shapespec")
    assert not s.validate((4, "4"))
    assert not s.validate((4, None))
    assert not s.validate((None,))
    assert not s.validate(())
    assert not s.validate((4,))
    assert s.validate((5, 4))
    assert s.validate((5, 0))
    assert s.validate((5, False))
    assert s.validate((5, 42098507180))
    assert not s.validate((5, 4, 0, 9))
