#!/usr/bin/env python3

# Module Docstring
"""
REST API FUNCTIONS

This module would account for all possible
functions for REST API testing.
"""

# Rest API Custom Libraries
from rest_api_exception import StringSpaceException

# Function for validation of palindrome
def is_string_palindrome(string_var):
    """
    Description:
        This is a function which helps you validate if a passed string
        is a palindrome.

    Arguments:
        string_var (str) :: Mandatory :: Example - hello

    Return:
        Type (bool) :: True for success ; False for failure

    Exception:
        StringSpaceException - If string passed has spaces

    Example:
        >>> is_string_palindrome("kayak")
        >>> True
        >>> is_string_palindrome("splunk")
        >>> False
    """
    # Validate if the user has sent a string as an arg
    if isinstance(string_var, str):

        # Validate the string passed has no spaces
        if len(string_var.split(" ")) > 1:
            raise StringSpaceException("String can only be a single word without spaces!")

    # Reverse the string
    reverse_var = ''.join(reversed(string_var))

    # Check if reverse equals string
    return string_var == reverse_var
    