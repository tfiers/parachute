from parachute import DimSize


def test_dimspec_any():
    s = DimSize(None)
    assert not s.is_valid("not a dimspec")
    assert not s.is_valid(None)
    assert not s.is_valid(DimSize)
    assert s.is_valid(4)
    assert s.is_valid(42098507180)
    assert s.is_valid(False)
    assert s.is_valid(True)


def test_dimspec_concrete():
    s = DimSize(4)
    assert not s.is_valid("not a dimspec")
    assert not s.is_valid(None)
    assert not s.is_valid(DimSize)
    assert s.is_valid(4)
    assert not s.is_valid(42098507180)
    assert not s.is_valid(False)
    assert not s.is_valid(True)
