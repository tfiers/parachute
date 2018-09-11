from parachute import ShapeSpec


def test_shapespec_any():
    s = ShapeSpec(None)
    assert not s.conforms("not a shapespec")
    assert not s.conforms((4, "4"))
    assert not s.conforms((4, None))
    assert not s.conforms((None,))
    assert s.conforms(())
    assert s.conforms((4,))
    assert s.conforms((5, 4))
    assert s.conforms((5, 0))
    assert s.conforms((5, False))
    assert s.conforms((5, 42098507180))


def test_shapespec_fix():
    s = ShapeSpec((5, 4))
    assert not s.conforms("not a shapespec")
    assert not s.conforms((4, "4"))
    assert not s.conforms((4, None))
    assert not s.conforms((None,))
    assert not s.conforms(())
    assert not s.conforms((4,))
    assert s.conforms((5, 4))
    assert not s.conforms((5, 0))
    assert not s.conforms((5, False))
    assert not s.conforms((5, 42098507180))


def test_shapespec_wildcard():
    s = ShapeSpec((5, None))
    assert not s.conforms("not a shapespec")
    assert not s.conforms((4, "4"))
    assert not s.conforms((4, None))
    assert not s.conforms((None,))
    assert not s.conforms(())
    assert not s.conforms((4,))
    assert s.conforms((5, 4))
    assert s.conforms((5, 0))
    assert s.conforms((5, False))
    assert s.conforms((5, 42098507180))
