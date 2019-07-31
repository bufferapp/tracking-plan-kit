import re
CAMEL_CASE_TEST_RE = re.compile(r'[a-z]+[A-Z0-9][a-z0-9]+[A-Za-z0-9]*|^[a-z0-9]+[a-z0-9]*')

def is_string(obj):
    """
    Checks if an object is a string.
    :param obj: Object to test.
    :return: True if string, false otherwise.
    :rtype: bool
    """
    return isinstance(obj, str)


def is_full_string(string):
    """
    Check if a string is not empty (it must contains at least one non space character).
    :param string: String to check.
    :type string: str
    :return: True if not empty, false otherwise.
    """
    return is_string(string) and string.strip() != ''


def is_camel_case(string):
    """
    Checks if a string is formatted as camel case.
    A string is considered camel case when:
    - it's composed only by letters ([a-zA-Z]) and optionally numbers ([0-9])
    - it contains both lowercase and uppercase letters
    - it does not start with a number
    :param string: String to test.
    :type string: str
    :return: True for a camel case string, false otherwise.
    :rtype: bool
    """
    return is_full_string(string) and bool(CAMEL_CASE_TEST_RE.match(string))