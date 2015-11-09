# -*- coding: utf-8 -*-
"""
Converts any integer into a base [BASE] number. I have chosen 62
as it is meant to represent the integers using all the alphanumeric
characters, [no special characters] = {0..9}, {A..Z}, {a..z}

I plan on using this to shorten the representation of possibly long ids,
a la url shortenters

saturate() takes the base 62 key, as a string, and turns it back into an integer
dehydrate() takes an integer and turns it into the base 62 string

https://gist.github.com/778542
"""
import math

BASE = 62

UPPERCASE_OFFSET = int(55)
LOWERCASE_OFFSET = int(61)
DIGIT_OFFSET = int(48)


def true_ord(char):
    """
    Turns a digit [char] in character representation
    from the number system with base [BASE] into an integer.
    :type char: char
    :rtype: ord
    """
    if char.isdigit():
        return ord(char) - DIGIT_OFFSET
    elif 'A' <= char <= 'Z':
        return ord(char) - UPPERCASE_OFFSET
    elif 'a' <= char <= 'z':
        return ord(char) - LOWERCASE_OFFSET
    else:
        raise ValueError("%s is not a valid character" % char)


def true_chr(integer):
    """
    Turns an integer [integer] into digit in base [BASE]
    as a character representation.

    :type integer: int
    """
    if integer < 10:
        try:
            return chr(integer + DIGIT_OFFSET)
        except TypeError:
            assert False, integer
    elif 10 <= integer <= 35:
        return chr(integer + UPPERCASE_OFFSET)
    elif 36 <= integer < 62:
        return chr(integer + LOWERCASE_OFFSET)
    else:
        raise ValueError("{0} is not a valid integer in the range of base {1}".format(integer, BASE))


def saturate(key):
    """
    Turn the base [BASE] number [key] into an integer

    :type key: []
    """
    int_sum = 0
    reversed_key = key[::-1]
    for idx, char in enumerate(reversed_key):
        int_sum += true_ord(char) * int(math.pow(BASE, idx))
    return int_sum


def dehydrate(integer):
    """
    Turn an integer [integer] into a base [BASE] number
    in string representation
    :type integer: int
    """
    # we won't step into the while if integer is 0
    # so we just solve for that case here
    if integer == 0:
        return '0'
    string = ""
    while integer > 0:
        remainder = integer % BASE
        string = '{0}{1}'.format(true_chr(remainder), string)
        integer = int(integer / BASE)
    return string


def url_normalize(url):
    """
    Deprecated: apps must normalize the URLs, if needed

    :type url: unicode
    """
    del url
    raise DeprecationWarning("Apps must now handle URL normalisation themselves")
