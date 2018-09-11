from parachute import DimSize


def test_dimspec_any():
    s = DimSize(None)
    assert not s.validate("not a dimspec")
    assert not s.validate(None)
    assert not s.validate(DimSize)
    assert s.validate(4)
    assert s.validate(42098507180)
    assert s.validate(False)
    assert s.validate(True)


def test_dimspec_concrete():
    s = DimSize(4)
    assert not s.validate("not a dimspec")
    assert not s.validate(None)
    assert not s.validate(DimSize)
    assert s.validate(4)
    assert not s.validate(42098507180)
    assert not s.validate(False)
    assert not s.validate(True)
