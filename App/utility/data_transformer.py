import csv
import requests
import json

username = 'optipark'  # Username for the API
password = 'Dyb1yoTU4TG8'  # Password for the API

path_to_links = '../../Data/Urls.json'  # Path to the json file with the API access links
path_to_csv = '../../Data/Location_Data.csv'  # Path to the csv file containing the location data


def add_location(dic, url):
    """
    This function adds the location to the json file and updates the csv file.

    Parameters
    ----------
    dic : dict
        Dictionary containing the characteristics of the location.
    url : str
        The url for the location-API.
    """

    add_link_to_json(dic['location'], url)  # Add the link to the json file

    update_csv()  # Update the csv file


def update_csv():
    """
    This function updates the csv file containing the locations of the facilities with the information from the urls.
    """

    locations, urls = get_locations_and_urls()  # Get the list of locations and the list of urls

    first_row = True  # Create boolean variable to write the header

    with open(path_to_csv, 'w', newline='') as csvfile:  # Open the csv file

        writer = csv.writer(csvfile, delimiter=',')  # Create a csv writer

        for location, url in zip(locations, urls):  # Iterate over the locations and the urls

            data = access_api(url)  # Extract the information from the url

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

    with open(path_to_links, 'r') as f:  # Open the json file with the API access links
        content = json.load(f)  # Load the content of the json file

    locations = []  # Create an empty list for the locations

    urls = []  # Create an empty list for the urls

    for key, value in content.items():  # Iterate over the keys and values of the dictionary
        locations.append(key)  # Add the location to the list
        urls.append(value)  # Add the url to the list

    return locations, urls  # Return the list of locations and the list of urls


def access_api(url):
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

    r = requests.get(url, auth=(username, password))  # Send a request to the url using the username and password

    if r.status_code != 200:  # If the request was not successful
        raise Exception('Could not access the url {}'.format(url))  # Raise an exception and print the url

    data = r.json()  # Extract the json data

    return data[0]  # Return the first element of the list (that is, the dictionary)


def delete_link_in_json(location):
    """
    This function deletes the link for the location from the json file.

    Parameters
    ----------
    location : str
        The location for which the link should be deleted.
    """

    with open(path_to_links, 'r') as f:  # Open the json file with the information about the locations
        content = json.load(f)  # Load the content of the json file

    del content[location]  # Delete the link for the location

    with open(path_to_links, 'w') as f:  # Open the json file with the information about the locations
        json.dump(content, f, indent=4)  # Write the new content to the json file


def add_link_to_json(location, url):
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

    with open(path_to_links, 'r') as f:  # Open the json file with the information about the locations
        content = json.load(f)  # Load the content of the json file

    content[location] = url  # Add the link for the location

    with open(path_to_links, 'w') as f:  # Open the json file with the information about the locations
        json.dump(content, f, indent=4)  # Write the new content to the json file
