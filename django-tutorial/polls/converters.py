""" Custom Path Converters

For more complex routing table matching requirements, you can define
custom path converters. A Converter is a class that:

1. has a regex as a string as an attribute (which will be compiled)
2. implements a to_python() method which converts the matched string
   into the type that should be passed into the view function. It
   should raise a ValueError if it cant convert the given value.
   A ValueError is interpreted as no match and will lead to a 404
   response unless another URL pattern matches
3. implements a to_url() method which handles converting the Python
   type into a string to be used in the URL. It should raise a
   ValueError if it cant convert the given value. A ValueError is
   interpreted as no match and as a consequence, reverse() will
   raise NoReverseMatch unless another URL pattern matches


Note:
    py3k f-string formatting. finally a world without .format()

    >>> a = 3
    >>> f'{a:3d}'
    '  3'
    >>> f'{a:<3d}'
    '3  '
    '  3'
    A
    >>> f'{a:^3d}'
    ' 3 '
    >>> f'{a:0^3d}'
    '030'
    >>> f'{a:03d}'
    >>> a = 'NaN'
    >>> f'{a:03d}'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: Unknown format code 'd' for object of type 'str'

"""


class FourDigitYearConverter:
    """ match url tokens that have exactly 4 digits in them

    Attributes:
        regex (str): python regular expression to compile and match
    """
    regex = '[0-9]{4}'

    def to_python(self, value):
        """ return an integer type for use in python
        Args:
            value (str): requested URLconf token token

        Returns:
            int: the token as an integer if possible

        Raises:
            ValueError: If value cannot be formatted as an integer.
                This appropriately prevents URLconf from matching.
        """
        return int(value)

    def to_url(self, value):
        return f'{value:0>4d}'


class TwoToFourDigitYearConverter:
    """ match url tokens that have at least 2 and at most 4 digits in them

    Attributes:
        regex (str): python regular expression to compile and match

    Note:
        This is effectively what Django will do with this regex

    >>> import re
    >>> regex = '[0-9]{1,4}'
    >>> test = re.compile(regex)
    >>> test.match('202')
    <re.Match object; span=(0, 3), match='202'>
    >>> test.match('202456')
    <re.Match object; span=(0, 4), match='2024'>
    >>> test.match('')
    >>> test.match('2')
    <re.Match object; span=(0, 1), match='2'>
    """
    regex = '[0-9]{2,4}'

    def to_python(self, value):
        """
        Args:
            value (str): url token to match

        Returns:
            str: the token pre padded with zeros if fewer than 4 digits

        Raises:
            ValueError: If value cannot be formatted as an integer.
                This appropriately prevents URLconf from matching.

        Todo:
            * negative value inputs can be formatted which will match

        """
        print(f"-->OneToFourDigitYearConverter({value})")
        return f'{value:0>4s}'

    def to_url(self, value):
        return f'{value:0>4s}'


