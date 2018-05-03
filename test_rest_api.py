#!/usr/bin/env python3

# Module Docstring
"""
REST API V1 TEST

This is a test module which would allow you to test rest api.
It will be a series of test cases which are based on business requirements
and additional requirements.
"""

# Python Standard Libraries
from unittest import TestCase, main, expectedFailure
from copy import deepcopy
import requests

# Python Addon Libraries
from django.core.validators import URLValidator as url
from django.core.exceptions import ValidationError
from ddt import ddt, data, unpack

# Rest API Custom Libraries
from rest_api_functions import is_string_palindrome as check_palindrome

@ddt
class MoviesRestApi(TestCase):
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
        self.base_url = "https://splunk.mocklab.io/movies"

        self.headers = {"Accept" : "application/json"}
        self.output = requests.get(url=self.url, headers=self.headers)
        self.results = self.output.json()["results"]

        # This would enable to check the entire diff
        # between attribute comparisons
        self.maxDiff = None # pylint: disable=C0103

    def tearDown(self):
        """
        This is a method that cleans up after every test case.
        """
        self.output = None
        self.results = None
        self.url = None
        self.base_url = None
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

    def test_genre_ids_sum(self):
        """
        Requirements:
        SPL-004: The number of movies whose sum of "genre_ids" > 400 should be no more than 7.
                 Another way of saying this is: there at most 7 movies such that
                 their sum of genre_ids is great than 400
        """
        # Declare a variable to store the number of movies
        # greater than 400
        movies_above_genre_ids_400 = 0

        # Iterate through each of the movie dict in the result list
        for each_movie in self.results:
            # Declare variable to store the sum of genre ids
            sum_of_genre_ids = 0

            # Add all genre ids for a movie
            for genre_id in each_movie["genre_ids"]:
                sum_of_genre_ids += genre_id

            # Check if it above 400
            if sum_of_genre_ids > 400:
                movies_above_genre_ids_400 += 1

        # Validate per the requirement
        self.assertLess(movies_above_genre_ids_400, 7, \
        msg="There can be only 7 movies above 400 as their sum of genre_ids")

    def test_palindrome_check(self):
        """
        Requirements:
        SPL-005: There is at least one movie in the database whose title has a palindrome in it.
                 Example: "title" : "Batman: Return of the Kayak Crusaders"
                 The title contains ‘kayak’ which is a palindrome.
        """
        # Declare a variable for counting palindrome occurances
        movie_titles_with_palindrome = 0

        # Iterate through each of the movie dict in the result list
        for each_movie in self.results:

            # Iterate through each word in the movie
            for each_word_in_movie in each_movie["title"].split(" "):

                # Check if it is a palindrome
                if check_palindrome(each_word_in_movie):
                    movie_titles_with_palindrome += 1

        # Per the requirement, validate the count is atleast ONE
        self.assertGreaterEqual(movie_titles_with_palindrome, 1, \
        msg="There should be at least 1 movie with a palindrome string in its title")

    def test_movie_name_is_substr(self):
        """
        Requirements:
        SPL-006: There are at least two movies in the database whose title contain
                 the title of another movie. Example: movie id: 287757
                 (Scooby-Doo Meets Dante), movie id: 404463 (Dante). This example
                 shows one such set. The business requirement is that there are
                 at least two such occurrences.
        """
        # Declare a variable for counting movie titles with substr occurances
        movie_count_with_substr = 0

        # Use List Comprehensions to build the list of titles
        movie_list = [each["title"] for each in self.results]

        # Iterate through each of the movie dict in the result list
        for each_movie in movie_list:

            # Use deepcopy to create a reference list
            movie_list_new = deepcopy(movie_list)

            # Remove the current movie title from reference list
            movie_list_new.remove(each_movie)

            # Iterate through each of the movie dict in the reference list
            for each_remaining_movie in movie_list_new:

                # Check if it is a substr in the movie from the reference list
                if each_movie in each_remaining_movie:
                    movie_count_with_substr += 1

        # Per the validation requirement, check if there are at least TWO titles
        self.assertLess(2, movie_count_with_substr, \
        msg="There needs to be atleast two titles which have substr")

    def test_sorting(self):
        """
        Requirements:
        SPL-003: Sorting requirement.
                 Rule #1 Movies with genre_ids == null should be first in response.
                 Rule #2, if multiple movies have genre_ids == null,
                 then sort by id (ascending). For movies that have non-null
                 genre_ids, results should be sorted by id (ascending)
        """
        # Declare movie list for required list, null genre_id list and non null genre_id list
        required_sorted_movie_list, genre_ids_with_null_list, genre_ids_not_null_list = [], [], []

        # Iterate through each of the movies dicts in the result list
        for each_movie in self.results:

            # If genre_id is empty then add to null list
            if each_movie["genre_ids"] == []:
                genre_ids_with_null_list.append(each_movie)
            else:
                # If genre_id is not empty then add to not null list
                genre_ids_not_null_list.append(each_movie)

        # Sort each lists by id
        genre_ids_with_null_list = sorted(genre_ids_with_null_list, key=lambda k: k['id'])
        genre_ids_not_null_list = sorted(genre_ids_not_null_list, key=lambda k: k['id'])

        # Place the null list before not null list
        required_sorted_movie_list = genre_ids_with_null_list + genre_ids_not_null_list

        # Validate the requirement order
        self.assertListEqual(required_sorted_movie_list, self.results)

    def test_post_with_data(self):
        """
        Requirements:
        Check the rest api implementation to see if data values affect the output.

        Expected Failures:
        When data value is None, {"name":"spiderman"}, {"description":"Return of the superhero"}
        """
        # Headers for POST request
        headers = {"Content-Type":"application/json"}

        # Data for POST request
        data_value_dict = {"name":"spiderman", "description":"Return of the superhero"}

        # Call the REST API
        output = requests.post(url=self.base_url, headers=headers, data=data_value_dict)

        # Validate if our POST request was Successful
        self.assertEqual(output.status_code, 200, \
        msg="Data value with \" {} \" does NOT work!".format(data_value_dict))

    @data("None", {"name":"spiderman"},\
    {"description":"Return of the superhero"})
    @expectedFailure
    def test_post_with_data_expfail(self, data_value):
        """
        Requirements:
        Check the rest api implementation to see if data values affect the output.

        Expected Failures:
        When data value is None, {"name":"spiderman"}, {"description":"Return of the superhero"}
        """
        # Headers for POST request
        headers = {"Content-Type":"application/json"}

        # Call the REST API
        output = requests.post(url=self.base_url, headers=headers, data=data_value)

        # Validate if our POST request was Successful
        self.assertEqual(output.status_code, 200, \
        msg="Data value with \" {} \" does NOT work!".format(data_value))

    @data("None", {"Accept":"application/json"})
    @expectedFailure
    def test_post_with_header_expfail(self, header_value):
        """
        Requirements:
        Check the rest api implementation to see if header values affect the output.

        Expected Failures:
        When header value is None and {"Accept":"application/json"}
        """
        # Data for POST request
        new_data_value = {"name":"spiderman", "description":"Return of the superhero"}

        # Call the REST API
        output = requests.post(url=self.base_url, headers=header_value, data=new_data_value)

        # Validate if our POST request was Successful
        self.assertEqual(output.status_code, 200, msg="Header value\
            with \" {} \" does NOT work!".format(header_value))

    @data({"Content-Type":"application/json"}, \
    {"Accept":"application/json", "Content-Type":"application/json"})
    def test_post_with_header_manip(self, header_value):
        """
        Requirements:
        Check the rest api implementation to see if header values affect the output.

        Expected Failures:
        When header value is None and {"Accept":"application/json"}
        """
        # Data for POST request
        new_data_value = {"name":"spiderman", "description":"Return of the superhero"}

        # Call the REST API
        output = requests.post(url=self.base_url, headers=header_value, data=new_data_value)

        # Validate if our POST request was Successful
        self.assertEqual(output.status_code, 200, msg="Header value\
            with \" {} \" does NOT work!".format(header_value))

    @data([{"name":"spiderman", "description":"Return of the superhero"},\
    {"Content-Type":"application/json"}],\
    [{"name":"spiderman", "description":"Return of the superhero"},\
    {"Accept":"application/json", "Content-Type":"application/json"}])
    @unpack
    def test_post_with_combo_manip(self, data_value, header_value):
        """
        Requirements:
        Check the rest api implementation to see if header values affect the output.
        """
        # Call the REST API
        output = requests.post(url=self.base_url, headers=header_value, data=data_value)

        # Validate if our POST request was Successful
        self.assertEqual(output.status_code, 200, \
            msg="Header value with \"{}\" and \
            Data value with \"{}\" does NOT work!".format(header_value, data_value))

    @data(["None", "None"], ["None", {"Accept":"application/json"}],\
    ["None", {"Content-Type":"application/json"}], \
    ["None", {"Accept":"application/json", "Content-Type":"application/json"}], \
    [{"name":"spiderman"}, "None"], \
    [{"name":"spiderman"}, {"Accept":"application/json"}], \
    [{"name":"spiderman"}, {"Content-Type":"application/json"}], \
    [{"name":"spiderman"}, {"Accept":"application/json",\
    "Content-Type":"application/json"}], \
    [{"name":"spiderman", "description":"Return of the superhero"}, "None"], \
    [{"name":"spiderman", "description":"Return of the superhero"},\
    {"Accept":"application/json"}], \
    )
    @unpack
    @expectedFailure
    def test_post_with_combo_expfail(self, data_value, header_value):
        """
        Requirements:
        Check the rest api implementation to see if header values affect the output.

        Expected Failures:
        When data value is None, {"name":"spiderman"}, {"description":"Return of the superhero"}
        When header value is None and {"Accept":"application/json"}
        """
        # Call the REST API
        output = requests.post(url=self.base_url, headers=header_value, data=data_value)

        # Validate if our POST request was Successful
        self.assertEqual(output.status_code, 200, \
            msg="Header value with \"{}\" and \
            Data value with \"{}\" does NOT work!".format(header_value, data_value))

    def test_check_new_movie(self):
        """
        Requirements:
        Check the rest api implementation to see if the newly added movie is present.
        """
        # Use custom url
        self.base_url = "{}?q=spiderman".format(self.base_url)

        # Pass GET request headers
        output = requests.get(url=self.base_url, headers=self.headers)

        # Fetch the output json
        results = output.json()["results"]

        # Use List Comprehension to fetch a list of movie titles
        movie_list = [each["title"] for each in results]

        # Validate the addition of new movie
        self.assertIn("spiderman", movie_list)

    @data("spiderman", "batman")
    def test_get_url_manip(self, movie):
        """
        Requirements:
        Check the rest api implementation to see if
        the output is filtered based on movie name.

        Assumptions:
        Spiderman has been added.

        Expected Failures:
        When movie is "splunk"
        """
        # Use custom url
        manip_url = "{}?q={}".format(self.base_url, movie)

        # Pass GET request headers
        output = requests.get(url=manip_url, headers=self.headers)

        # Validate if our POST request was Successful
        self.assertEqual(output.status_code, 200,\
            msg="Movie value with \"{}\" does NOT work!".format(movie))

    @expectedFailure
    def test_get_url_manip_exp_fail(self, movie="splunk"):
        """
        Requirements:
        Check the rest api implementation to see if the
        output is filtered based on movie name splunk.

        Assumptions:
        Splunk movie are not added
        """
        # Use custom url
        self.base_url = "{}?q={}".format(self.base_url, movie)

        # Pass GET request headers
        output = requests.get(url=self.base_url, headers=self.headers)

        # Validate if our POST request was Successful
        self.assertEqual(output.status_code, 200, \
            msg="Movie value with \"{}\" does NOT work!".format(movie))

    @data(1, 2, 4, 8, 16)
    def test_verify_movie_count(self, counter):
        """
        Requirements:
        Check the rest api implementation to see if the output count of movies
        is same as what we pass in the payload
        """
        payload = {"count" : counter}

        # Pass GET request headers
        output = requests.get(url=self.url, headers=self.headers, params=payload)

        # Fetch the output json
        results = output.json()["results"]

        # Validate if our POST request was Successful
        self.assertEqual(output.status_code, 200)

        # Validate if our POST request had the exact count
        self.assertEqual(results.__len__(), payload["count"], \
        msg="Obs Count \"{}\" Exp Count \"{}\"".format(payload["count"], results.__len__()))

if __name__ == "__main__":
    main()
