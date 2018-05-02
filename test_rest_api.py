#!/usr/bin/env python3

# Module Docstring
"""
REST API V1 TEST

This is a test module which would allow you to test rest api.
It will be a series of test cases which are based on business requirements
and additional requirements.
"""

# Python Standard Libraries
import unittest
import requests

# Python Addon Libraries
from django.core.validators import URLValidator as url
from django.core.exceptions import ValidationError

class MoviesRestApi(unittest.TestCase):
    """
    MovieRestApi module is based on Unittest.
    It has a setUp and tearDown which would
    take care of all the test cases.

    Sample execution command:-
    python3 test_rest_api.py

    Specific test execution:-
    python3 test_rest_api.py MoviesRestApi.test_image_poster_path_validation()

    """
    def setUp(self):
        """
        This is a method which helps in running the request for every test case.
        """
        # URL for the REST API call
        self.url = "https://splunk.mocklab.io/movies?q=batman"

        self.headers = {"Accept" : "application/json"}
        self.output = requests.get(url=self.url, headers=self.headers)
        self.results = self.output.json()["results"]

    def tearDown(self):
        """
        This is a method that cleans up after every test case.
        """
        self.output = None
        self.results = None
        self.url = None
        self.headers = None

    def test_image_path_validation(self):
        """
        Requirements:
        SPL-001: No two movies should have the same image

        Assumptions:
        1. poster_path means image
        2. poster_path key can be absent
        3. poster_path key can be None/Null
        """
        # Poster path list variable
        poster_path_list = []

        # Iterate through each of the movie dict in the result list
        for each_movie in self.results:

            # Use sub test to differentiate failures
            with self.subTest(each_movie["title"]):

                # Add the poster_path to the poster_path_list
                try:
                    if each_movie["poster_path"]:
                        poster_path_list.append(each_movie["poster_path"])
                    else:
                        # This is done because sorting does not work with None & str
                        poster_path_list.append("None")
                except KeyError:
                    # No poster_path or null is acceptable
                    pass

        # Unique list of poster_path_list
        unique_poster_path_list = sorted(list(set(poster_path_list)))

        poster_path_list = sorted(poster_path_list)

        # Assert if lists are equal
        self.assertListEqual(unique_poster_path_list, \
        poster_path_list, msg="Both lists don't match")

    def test_poster_url_validation(self):
        """
        Requirements:
        SPL-002: All poster_path links must be valid. poster_path link of null is also acceptable

        Assumptions:
        1. poster_path key can be absent
        2. poster_path key can be None/Null
        """
        # Poster path list variable
        validate = url()

        # Iterate through each of the movie dict in the result list
        for each_movie in self.results:
            # Use sub test to differentiate failures
            with self.subTest(each_movie["title"]):
                try:
                    validate(each_movie["poster_path"])
                except ValidationError:
                    self.fail(msg="Url Validation Failed for movie title \"" + \
                    each_movie["title"] + "\" with url \"" + each_movie["poster_path"] + "\"")
                except KeyError:
                    # No poster_path is acceptable
                    pass
                except AttributeError:
                    # Assuming poster path of null is acceptable
                    pass

if __name__ == "__main__":
    unittest.main()
