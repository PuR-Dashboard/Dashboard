import csv
import requests
import json

from requests import Response

username = 'optipark'  # Username for the API
password = 'Dyb1yoTU4TG8'  # Password for the API

path_to_urls = '../../Data/Urls.json'  # Path to the json file with the API access links
path_to_csv = '../../Data/Location_Data.csv'  # Path to the csv file containing the location data
path_to_characteristics = '../../Data/Characteristics.csv'  # Path to the csv file containing the characteristics of the
# locations


# --- DEPRECATED --- #

def update_csv() -> None:
    """
    This function updates the csv file containing the locations of the facilities with the information from the urls.
    """

    locations, urls = get_locations_and_urls()  # Get the list of locations and the list of urls

    first_row = True  # Create boolean variable to write the header

    with open(path_to_csv, 'w', newline='') as csvfile:  # Open the csv file

        writer = csv.writer(csvfile, delimiter=',')  # Create a csv writer

        for location, url in zip(locations, urls):  # Iterate over the locations and the urls

            data = get_dict_from_api(url)  # Extract the information from the url

            if first_row:  # If it is the first row
                header = list(data)  # Get the keys of the dictionary

                header.remove('geometry')  # Remove the geometry key from the header

                header = ['location', 'lat', 'lon'] + header  # Add the location, lat and lon keys to the header

                writer.writerow(header)  # Write the header

                first_row = False  # Set the first_row variable to False

            point = data['geometry']  # Get the coordinates of the location

            split = point.split(' ')  # Split the string at the space

            lat = float(split[1][1:])  # Remove the '(' from the latitude and convert to float
            lon = float(split[2][:-1])  # Remove the ')' from the longitude and convert to float

            values = list(data.values())  # Get the values of the dictionary

            values.remove(point)  # Remove the point from the values

            writer.writerow([location, lat, lon] + values)  # Write the row to the csv file


def get_locations_and_urls() -> (list, list):
    """
    This function returns the list of all locations and their corresponding urls.

    Returns:
        Tuple containing the list of locations and the list of urls.
    """

    with open(path_to_urls, 'r') as f:  # Open the json file with the API access links
        content = json.load(f)  # Load the content of the json file

    locations = []  # Create an empty list for the locations

    urls = []  # Create an empty list for the urls

    for key, value in content.items():  # Iterate over the keys and values of the dictionary
        locations.append(key)  # Add the location to the list
        urls.append(value)  # Add the url to the list

    return locations, urls  # Return the list of locations and the list of urls


# --- General functions --- #

def add_location(dic, url) -> None:
    """
    This function adds the location with the corresponding url for the API access to the Urls.json file and adds the
    location with its corresponding characteristics to the Characteristics.csv file.

    Parameters
    ----------
    dic : dict
        Dictionary containing the characteristics of the location.
    url : str
        The url for the location-API.

    Raises
    ------
    Exception
        If the location already exists.
    """

    if not check_location_exists(dic['location']):  # If the location does not exist yet
        # --- Add the location and its api-access to the Urls.json file --- #
        add_url_to_json(dic['location'], url)  # Add the link to the json file

        # --- Append the location with its characteristics to the csv file --- #
        with open(path_to_characteristics, 'a', newline='') as characteristics_file:  # Open the csv file

            writer = csv.writer(characteristics_file, delimiter=',')  # Create a csv writer

            writer.writerow([dic['location'], get_lat_lon_from_url(url)] + list(dic.values())[1:])  # Write the location
            # and its characteristics

            characteristics_file.close()  # Close the file

    else:  # If the location already exists
        raise Exception('The location {} already exists'.format(dic['location']))  # Raise an exception


def remove_location(location: str) -> None:
    """
    This function removes the location from the json file and the csv file.

    Parameters
    ----------
    location : str
        The location that should be removed.
    """

    if check_location_exists(location):  # If the location exists
        remove_location_from_json(location)  # Remove the location from the json file

        remove_location_from_csv(location)  # Remove the location from the csv file

    else:  # If the location does not exist
        raise Exception('The location {} does not exist'.format(location))  # Raise an exception


def check_location_exists(location: str) -> bool:
    """
    This function checks if the location exists in the json file. If there is an entry in the Urls.json file for the
    location, the function returns True. Otherwise, it returns False.

    Parameters
    ----------
    location : str
        The location for which should be checked if it exists.

    Returns
    -------
    exists : bool
        Boolean indicating if the location exists.
    """

    with open(path_to_urls, 'r') as f:  # Open the json file with the information about the locations
        content = json.load(f)  # Load the content of the json file

    return location in content  # Check and return if the location exists in the json file


# --- Functions for the Urls.json file --- #

def remove_location_from_json(location: str) -> None:
    """
    This function deletes the link for the location from the json file.

    Parameters
    ----------
    location : str
        The location for which the link should be deleted.
    """

    with open(path_to_urls, 'r') as f:  # Open the json file with the information about the locations
        content = json.load(f)  # Load the content of the json file

    del content[location]  # Delete the link for the location

    with open(path_to_urls, 'w') as f:  # Open the json file with the information about the locations
        json.dump(content, f, indent=4)  # Write the new content to the json file


def update_url_in_json(location: str, url: str) -> None:
    """
    This function updates the link for the location in the json file.

    Parameters
    ----------
    location : str
        The location for which the link should be updated.
    url : str
        The new url for the location.
    """

    add_url_to_json(location, url)  # Update the link in the json file by calling the add_link_to_json function


def add_url_to_json(location: str, url: str) -> None:
    """
    This function adds the link for the location to the json file. Can also be used to update the link of the given
    location.

    Parameters
    ----------
    location : str
        The location for which the link should be added.
    url : str
        The url for the location.
    """

    with open(path_to_urls, 'r') as f:  # Open the json file with the information about the locations
        content = json.load(f)  # Load the content of the json file

    content[location] = url  # Add the link for the location

    with open(path_to_urls, 'w') as f:  # Open the json file with the information about the locations
        json.dump(content, f, indent=4)  # Write the new content to the json file


# --- Functions for the Characteristics.csv file --- #

def remove_location_from_csv(location: str) -> None:
    """
    This function removes the location from the csv file.

    Parameters
    ----------
    location : str
        The location that should be removed.
    """

    with open(path_to_characteristics, 'r') as f:  # Open the csv file
        reader = csv.reader(f)  # Create a csv reader
        lines = list(reader)  # Read the csv file

    with open(path_to_characteristics, 'w', newline='') as f:  # Open the csv file
        writer = csv.writer(f)  # Create a csv writer

        for line in lines:  # Iterate over the lines
            if line[0] != location:  # If the location is not the location that should be removed
                writer.writerow(line)  # Write the line to the csv file


def update_characteristics_in_csv(dic: dict) -> None:
    """
    This function updates the characteristics of the location in the csv file.

    Parameters
    ----------
    dic : dict
        Dictionary containing the new characteristics of the location.
    """

    location = dic['location']  # Get the location from the dictionary

    with open(path_to_characteristics, 'r') as f:  # Open the csv file
        reader = csv.reader(f)  # Create a csv reader
        lines = list(reader)  # Read the csv file

    with open(path_to_characteristics, 'w', newline='') as f:  # Open the csv file
        writer = csv.writer(f)  # Create a csv writer

        for line in lines:  # Iterate over the lines
            if line[0] == location:  # If the location is the location that should be updated
                writer.writerow([location, line[1], line[2]] + list(dic.values()))  # Write the new characteristics to
                # the csv file
            else:  # If the location is not the location that should be updated
                writer.writerow(line)  # Write the line to the csv file


# --- Functions for the API access --- #

def get_lat_lon_from_url(url: str) -> tuple[float, float]:
    """
    This function returns the latitude and longitude of the location given in the API.

    Parameters
    ----------
    url : str
        The url for the API access.

    Returns
    -------
    lat : float
        The latitude of the location.
    lon : float
        The longitude of the location.
    """

    data = get_dict_from_api(url)  # Access the API and get the dictionary with the information

    point = data['geometry']  # Get the coordinates of the location

    split = point.split(' ')  # Split the string at the space

    lat = float(split[1][1:])  # Remove the '(' from the latitude and convert to float
    lon = float(split[2][:-1])  # Remove the ')' from the longitude and convert to float

    return lat, lon  # Return the latitude and longitude in the url


def get_dict_from_api(url: str) -> dict:
    """
    This function extracts the information for the facility from the url.

    Parameters
    ----------
    url : str
        The url of the facility.

    Returns
    -------
    data : dict
        Dictionary containing the information for the facility.
    """

    request = get_response_from_url(url)  # Send a request to the url and get the response

    data = request.json()  # Extract the json data from the response

    return data[0]  # Return the first element of the list (that is, the dictionary)


def get_response_from_url(url: str) -> Response:
    """
    This function sends a request to the url and returns the response.

    Parameters
    ----------
    url : str
        The url for the request.

    Returns
    -------
    r : Response
        The response from the request.

    Raises
    ------
    Exception
        If the request is not successful.
    """

    r = requests.get(url, auth=(username, password))  # Send a request to the url using the username and password

    if r.status_code != 200:  # If the request was not successful
        raise Exception('Could not access the url {}'.format(url))  # Raise an exception and print the url

    return r  # Return the response
