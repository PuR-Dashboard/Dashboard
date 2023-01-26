import unittest
from App.utility.data_functions import *

class Data_Functions_Tester(unittest.TestCase):

    example_dict = {
            "location": "location name",
            "address": "address",
            "administration": "administration",
            "kind": "kind",
            "number_parking_lots": "number_parking_lots",
            "price": "price",
            "public_transport": "public_transport",
            "road_network_connection": "road_network_connection",
        }

    def test_add_location(self):

        # Test whether the function raises an exception when the url is not valid
        self.assertRaises(Exception, add_location, self.example_dict, "test") 

        # Test whether the function raises an exception when no dictionary is passed
        self.assertRaises(Exception, add_location, None, "https://www.google.com")

        # Test whether the function raises an exception when the dictionary is not a dictionary
        self.assertRaises(Exception, add_location, 5, "https://www.google.com")

        add_location(self.example_dict, "https://www.google.com")
        self.assertTrue(check_location_exists(self.example_dict["location"]))

        # Test whether the function raises an exception when the location is already existing 
        self.assertRaises(Exception, add_location, self.example_dict, "https://www.google.com")

        remove_location(self.example_dict["location"])

    def test_check_url(self):
        # Test whether the function raises an exception when the url is not valid
        self.assertRaises(Exception, check_url, "test")

        # Test whether the function raises an exception when no url is passed
        self.assertRaises(Exception, check_url, None)

        # Test whether the function raises an exception when the url is not a string
        self.assertRaises(Exception, check_url, 5)

        check_url("https://www.google.com")
        
    def test_check_location_exists(self):
        self.assertFalse(check_location_exists("fjkdlöafnioawe"))
        self.assertRaises(Exception, check_location_exists, None)
        self.assertRaises(Exception, check_location_exists, 5)

        add_url_to_json("test", "test")
        self.assertTrue(check_location_exists("test"))
        remove_location_from_json("test")

    def test_check_url(self):

        # Test whether the function raises an exception when no url is passed
        self.assertRaises(Exception, check_url, None)

        # Test whether the function raises an exception when the url is not a string
        self.assertRaises(Exception, check_url, 5)

        # Test whether the function raises an exception when the url is not valid
        self.assertRaises(Exception, check_url, "test")

        # Test whether the function raises an exception when the url is valid
        check_url("https://www.google.com")

    def test_remove_location(self):
        # Test whether the function raises an exception when the given location is not a string
        self.assertRaises(Exception, remove_location, None)

        self.assertRaises(Exception, remove_location, 5)

        self.assertRaises(Exception, remove_location, "djklfwsanfold")

        # Test whether the function raises an exception in general
        add_url_to_json("test", "test")
        remove_location("test")

    def test_remove_location_from_json(self):
        # Test whether the function raises an exception when the given location is not a string
        self.assertRaises(Exception, remove_location_from_json, None)

        self.assertRaises(Exception, remove_location_from_json, 5)

        self.assertRaises(Exception, remove_location_from_json, "djklfwsanfold")

        # Test whether the function raises an exception in general
        add_url_to_json("test", "test")
        remove_location_from_json("test")

    def test_update_url_in_json(self):
        # Test whether the function raises an exception when the given location is not a string
        self.assertRaises(Exception, update_url_in_json, None, "test")

        self.assertRaises(Exception, update_url_in_json, 5, "test")

        self.assertRaises(Exception, update_url_in_json, "djklfwsanfold", "test")

        # Test whether the function raises an exception when the given url is not a string
        self.assertRaises(Exception, update_url_in_json, "test", None)

        self.assertRaises(Exception, update_url_in_json, "test", 5)

        # Test whether the function raises an exception in general
        add_url_to_json("test", "test")
        update_url_in_json("test", "tset")
        self.assertEqual(get_url_from_json("test"), "tset")
        remove_location_from_json("test")

    def test_add_url_to_json(self):
        self.assertRaises(Exception, add_url_to_json, None, "test")
        self.assertRaises(Exception, add_url_to_json, "test", None)
        self.assertRaises(Exception, add_url_to_json, 5, "test")
        self.assertRaises(Exception, add_url_to_json, "test", 5)

        add_url_to_json("test", "test")
        self.assertEqual(get_url_from_json("test"), "test")
        self.assertTrue(check_location_exists("test"))
        remove_location_from_json("test")

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
