from abc import ABC


class Validator(ABC):
    pass


# Based on this excellent writeup on metaclasses:
# https://stackoverflow.com/a/6581949/2611913
def set_validator_params(clsname, bases, attrs):
    attrs["jo"] = "test"
    # Create class using special `type()` call:
    return type(clsname, bases, attrs)


def either(*_options):
    class Option(Validator, metaclass=set_validator_params):
        options = _options

        def is_valid(self) -> bool:
            return self in self.options

        def _homogenous_type(self) -> bool:
            """ Whether all options are of the same type. """
            first_type = type(self.options[0])
            return all(type(option) == first_type for option in self.options)

    return Option
