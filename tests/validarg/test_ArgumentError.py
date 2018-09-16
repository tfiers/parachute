from parachute import ArgumentError


def my_function(array_size: int):
    pass


error = ArgumentError(my_function, "array_size", "99")

expected_msg = """Argument did not match parameter annotation.
Function       my_function
Parameter      array_size
Annotation     int
Argument       "99"
Argument type  str"""


def test_repr():
    assert str(error) == expected_msg
