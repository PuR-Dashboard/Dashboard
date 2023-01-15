import csv
import requests
import json
from datetime import datetime
from utility.util_functions import *
from requests import Response

username = 'optipark'  # Username for the API
password = 'Dyb1yoTU4TG8'  # Password for the API

path_to_urls = '../../Data/Urls.json'  # Path to the json file with the API access links
path_to_csv = '../../Data/Location_Data.csv'  # Path to the csv file containing the location data
path_to_characteristics = '../../Data/Characteristics.csv'  # Path to the csv file containing the characteristics of the
# locations
path_to_occupancy = '../../Data/Occupancy.csv'


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

            data = get_dict_from_url(url)  # Extract the information from the url

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


def get_locations_and_urls():
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

    location = dic['location']  # Get the location from the dictionary

    if True:#if not check_location_exists(location):  # If the location does not exist yet
        # --- Add the location and its api-access to the Urls.json file --- #
        #add_url_to_json(location, url)  # Add the link to the json file

        # --- Append the location with its characteristics to the csv file --- #
        with open(get_path_to_csv("Characteristics.csv"), 'a', newline='', encoding='utf-8-sig') as characteristics_file:  # Open the csv file

            writer = csv.writer(characteristics_file, delimiter=',')  # Create a csv writer
                                        #get_lat_lon_from_url(url)
            writer.writerow([location, 0, 0] + list(dic.values())[1:])  # Write the location
            # and its characteristics

            characteristics_file.close()  # Close the file

        # --- Append the location to the csv file containing the occupancies --- #
        #add_location_to_occ_csv(location)  # Add the location to the csv file containing the occupancies

    else:  # If the location already exists
        raise Exception('The location {} already exists'.format(location))  # Raise an exception


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

    with open(get_path_to_csv("Urls.json"), 'r') as f:  # Open the json file with the information about the locations
        content = json.load(f)  # Load the content of the json file

    content[location] = url  # Add the link for the location

    with open(get_path_to_csv("Urls.json"), 'w') as f:  # Open the json file with the information about the locations
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


# --- Functions for the Occupancy.csv file --- #

def update_location_occupancy(location: str) -> None:
    """
    This function updates the occupancy of the location. First, the function tries to read the occupancy of the given
    location from its url. If that was successful, the function updates the occupancy in the csv file. It appends a new
    line to the csv file with the current time stamp and the occupancy. For all other locations, the function simply
    appends the previous occupancy in the new row

    Parameters
    ----------
    location : str
        The location for which the occupancy should be updated.
    """

    if not check_location_exists(location):  # If the location does not exist
        raise Exception('The location {} does not exist'.format(location))  # Raise an exception

    with open(path_to_urls, 'r') as f:  # Open the json file with the information about the locations
        content = json.load(f)  # Load the content of the json file

    url = content[location]  # Get the url for the location

    dic = get_dict_from_url(url)  # Get the dictionary with the occupancy information from the url

    occupancy_tendency = dic['occupancy_tendency']  # Get the occupancy tendency from the dictionary

    # Open the input file in read mode and the output file in write mode
    with open('input.csv', 'r') as input_file, open('output.csv', 'w') as output_file:
        reader = csv.reader(input_file)  # Create a csv reader
        writer = csv.writer(output_file)  # Create a csv writer

        first_row = next(reader)  # Read the first row of the csv file
        last_row = None  # Initialize the last row

        for row in reader:  # Iterate over the rows
            last_row = row  # Set the last row to the current row
            writer.writerow(row)  # Write the row to the output file

        new_row = [datetime.now()]  # Initialize the new row with the current time stamp
        for i in range(1, len(first_row)):  # Iterate over the columns
            new_row.append(
                occupancy_tendency if first_row[i] == location else last_row[i]
            )  # Add the occupancy tendency to the new row if the column is the column for the location, otherwise add
            # the occupancy of the last row

        writer.writerow(new_row)  # Write the new row to the output file


def add_location_to_occ_csv(location: str) -> None:
    """
    This function adds the location to the occupancy csv file. Note that the location is added to the first row of the
    csv file. For every timestamp already existing in the csv file, the occupancy of the location is set to no value.

    Parameters
    ----------
    location : str
        The location that should be added.
    """

    with open(get_path_to_csv("Occupancy.csv"), 'r') as f, open(get_path_to_csv("Occupancy.csv"), 'w') as w:  # Open the csv file in read and write
        reader = csv.reader(f)  # Create a csv reader
        writer = csv.writer(w)  # Create a csv writer

        all_rows = []  # Create a list to store the lines of the csv file
        row = next(reader)  # Get the first row of the csv file
        row.append(location)  # Add the location to the row
        all_rows.append(row)  # Add the first row to the list

        for row in reader:  # Iterate over the rows of the csv file
            row.append('')  # Add an empty cell to the row
            all_rows.append(row)  # Add the row to the list

        writer.writerows(all_rows)  # Write the list to the csv file


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

    data = get_dict_from_url(url)  # Access the API and get the dictionary with the information

    point = data['geometry']  # Get the coordinates of the location

    split = point.split(' ')  # Split the string at the space

    lat = float(split[1][1:])  # Remove the '(' from the latitude and convert to float
    lon = float(split[2][:-1])  # Remove the ')' from the longitude and convert to float

    return lat, lon  # Return the latitude and longitude in the url


def get_dict_from_url(url: str) -> dict:
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


if __name__ == '__main__':
    update_location_occupancy('Zwingenberg')
