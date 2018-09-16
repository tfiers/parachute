from parachute import dimsize


def test_dimspec_any():
    DimSize = dimsize(None)
    assert not DimSize("not a dimspec").is_valid()
    assert not DimSize(None).is_valid()
    assert not DimSize(4.2).is_valid()
    assert not DimSize(DimSize).is_valid()
    assert DimSize(4).is_valid()
    assert DimSize(4.0).is_valid()
    assert DimSize(42098507180).is_valid()
    assert DimSize(False).is_valid()
    assert DimSize(True).is_valid()


def test_dimspec_concrete():
    DimSize = dimsize(4)
    assert not DimSize("not a dimspec").is_valid()
    assert not DimSize(None).is_valid()
    assert not DimSize(4.2).is_valid()
    assert not DimSize(DimSize).is_valid()
    assert DimSize(4).is_valid()
    assert DimSize(4.0).is_valid()
    assert not DimSize(42098507180).is_valid()
    assert not DimSize(False).is_valid()
    assert not DimSize(True).is_valid()


def test_repr():
    pairs = {
        None: "Array dimension size arbitrary.",
        4: "Array dimension size 4.",
    }
    for spec, string in pairs.items():
        assert dimsize(spec).get_annotation_str() == string
