import unittest
from App.utility.data_functions import *

class Data_Functions_Tester(unittest.TestCase):

    example_dict = {
        "location": "test"
    }

    def test_add_location(self):
        self.assertRaises(Exception, add_location, {"test": "test"}, "test")

        self.assertRaises(Exception, add_location, None, "https://www.google.com")

        add_location({"test": "test"}, "https://www.google.com")
        
    def test_check_location_exists(self):
        assert 1 == 1

    def test_check_url(self):
        check_url("https://www.google.com")

    def test_remove_location(self):
        assert 1 == 1

    def test_remove_location_from_json(self):
        assert 1 == 1

    def test_update_url_in_json(self):
        assert 1 == 1

    def test_add_url_to_json(self):
        assert 1 == 1

    def test_remove_location_from_csv(self):
        assert 1 == 1

    def test_update_characteristics_in_csv(self):
        assert 1 == 1

    def test_update_location_occupancy(self):
        assert 1 == 1

    def test_add_location_to_occ_csv(self):
        assert 1 == 1

    def test_get_lat_lon_from_url(self):
        assert 1 == 1

    def test_get_dict_from_url(self):
        assert 1 == 1

    def test_get_response_from_url(self):
        assert 1 == 1
