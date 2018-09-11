from parachute import DimensionSizeSpec


def test_dimspec_any():
    s = DimensionSizeSpec(None)
    assert not s.conforms("not a dimspec")
    assert not s.conforms(None)
    assert not s.conforms(DimensionSizeSpec)
    assert s.conforms(4)
    assert s.conforms(42098507180)
    assert s.conforms(False)
    assert s.conforms(True)


def test_dimspec_concrete():
    s = DimensionSizeSpec(4)
    assert not s.conforms("not a dimspec")
    assert not s.conforms(None)
    assert not s.conforms(DimensionSizeSpec)
    assert s.conforms(4)
    assert not s.conforms(42098507180)
    assert not s.conforms(False)
    assert not s.conforms(True)
