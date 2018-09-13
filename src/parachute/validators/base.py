from abc import ABC


class Validator(ABC):
    pass


def either(*_options):
    class Option(Validator):

        options = _options

        def is_valid(self) -> bool:
            return self in self.options

        def _homogenous_type(self) -> bool:
            """ Whether all options are of the same type. """
            first_type = type(self.options[0])
            return all(type(option) == first_type for option in self.options)

    return Option
