import csv
import requests
import json

# User credentials
username = 'optipark'
password = 'Dyb1yoTU4TG8'

# Path: Data/Urls.json
path_to_links = '../../Data/Urls.json'
# Path: Data/Location_Data.csv
path_to_csv = '../../Data/Location_Data.csv'


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

    # Add the link to the json file
    add_link_to_json(dic['location'], url)

    # Update the csv file
    update_csv()


def update_csv():
    """
    This function updates the csv file containing the locations of the facilities with the information from the urls.
    """

    # Get the locations and the urls
    locations, urls = get_locations_and_urls()

    # Create boolean variable to write the header
    first_row = True

    # Open the csv file
    with open(path_to_csv, 'w', newline='') as csvfile:

        # Create a csv writer
        writer = csv.writer(csvfile, delimiter=',')

        # Iterate over the locations and the urls
        for location, url in zip(locations, urls):

            # Extract the information from the url
            data = access_api(url)

            # Write the header
            if first_row:
                # Get the keys of the dictionary
                header = list(data)

                # Remove the geometry key from the header
                header.remove('geometry')

                # Add necessary keys to the header
                header = ['location', 'lat', 'lon'] + header

                # Write the header
                writer.writerow(header)

                # Set the first_row variable to False
                first_row = False

            # Get the coordinates of the location
            point = data['geometry']

            # Remove unnecessary characters from the coordinates
            split = point.split(' ')

            # Extract the latitude and longitude
            lat = float(split[1][1:])
            lon = float(split[2][:-1])

            # Create a list with the values of the dictionary
            values = list(data.values())

            # Remove the point from the values
            values.remove(point)

            # Write the location and the values for the location to the csv file
            writer.writerow([location, lat, lon] + values)


def get_locations_and_urls():
    """
    This function returns the list of all locations and their corresponding urls.

    Returns:
        Tuple containing the list of locations and the list of urls.
    """

    # Access the json file with the information about the locations
    with open(path_to_links, 'r') as f:
        content = json.load(f)

    # Create an empty list for the locations
    locations = []

    # Create an empty list for the urls of the locations
    urls = []

    # Iterate over the urls and extract the location from each one
    for key, value in content.items():
        locations.append(key)
        urls.append(value)

    # Return the list of locations and the list of urls
    return locations, urls


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

    # Send a request to the url using the username and password
    r = requests.get(url, auth=(username, password))

    # If the request was not successful, print the faulty url
    if r.status_code != 200:
        raise Exception('Could not access the url {}'.format(url))

    # Extract the information from the response
    data = r.json()

    # Return the information
    return data[0]


def delete_link_in_json(location):
    """
    This function deletes the link for the location from the json file.

    Parameters
    ----------
    location : str
        The location for which the link should be deleted.
    """

    # Access the json file with the information about the locations
    with open(path_to_links, 'r') as f:
        content = json.load(f)

    # Delete the link for the location
    del content[location]

    # Write the new content to the json file
    with open(path_to_links, 'w') as f:
        json.dump(content, f, indent=4)


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

    # Access the json file with the information about the locations
    with open(path_to_links, 'r') as f:
        content = json.load(f)

    # Add the link for the location
    content[location] = url

    # Write the new content to the json file
    with open(path_to_links, 'w') as f:
        json.dump(content, f, indent=4)
