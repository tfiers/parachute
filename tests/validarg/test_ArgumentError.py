from parachute import ArgumentError


def my_function(array_size: int):
    pass


error = ArgumentError(my_function, "array_size", "99")

# fmt: off
first_line = (
    "Argument `array_size` of my_function did not match its "
    "parameter annotation."
)
expected_msg = first_line + """

Annotation: int

Got argument of type `str` and value:
'99'"""
# fmt: on


def test_repr():
    assert str(error) == expected_msg
