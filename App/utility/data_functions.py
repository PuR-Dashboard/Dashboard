import csv
import requests
import json
import validators
from datetime import datetime

from requests import Response


import pandas as pd
import os
import pathlib
from collections import defaultdict




#-------------------
#util functions

#TO-DO: Error if while loop breaks and nothing matching was found
def get_root_dir(name_of_top_folder="App")-> str:
    """
    This function builds dynamically the directory to the parentfolder of the file we are searching independent of the folder depth.

    Parameters
    ----------
    name_of_top_folder : str
        Name of the topfolder of the file we want to have.

    Returns
    -------
    parent_path:
        The directory to the parentfolder of the file we are searching for.

    """
    current_path = pathlib.Path(__file__).parent.resolve()  # determining the current path
    parent_path = current_path

    while os.path.basename(parent_path) != name_of_top_folder: # searching for the given name_of_top_folder starting with the current path
        parent_path = parent_path.parent.absolute() # searching on depth deeper

        if parent_path.parent.absolute() == parent_path:  # if we found the corrcet name_of_top_folder we are stopping the search
            break


    parent_path = parent_path.parent.absolute()

    return parent_path


def get_path_to_csv(name_of_csv="Characteristics.csv", app_name="App")-> str:
    """
    This function builds dynamically the directory to the csv-file.

    Parameters
    ----------
    name_of_csv : str
        Name of the csv we are searching for.

    app_name:
        The name of the parent folder of the file we are searching for.

    Returns
    -------
    path:
        The directory to the csv file we are searching for.

    """
    data_path = get_root_dir(app_name) # determining the directory to the parent folder.

    return os.path.join(data_path, os.path.join("Data", name_of_csv)) # creating the path to the name_of_csv filr by joining the directory of the parent folder with the given name of the csv.



def get_data(name_of_csv="Location_Data.csv", app_name="App")-> pd.DataFrame:
    """
    This function stores all the data in a DataFrame which are stored in the given csv file.

    Parameters
    ----------
    name_of_csv : str
        Name of the csv we are searching for.

    app_name:
        The name of the parent folder of the file we are searching for.

    Returns
    -------
    df:
        The DataFrame with all the data of the csv File.

    """
    try:
        df = pd.read_csv(get_path_to_csv(name_of_csv, app_name))  #transforming the data of the csv in a dataframe.
    except:
        raise Exception("Fehler beim Daten auslesen!")
    return df

def get_image(location_name = " ") -> str:
    """
    This function returns you the image of a given location
    Parameters
    ----------
    location_name: str
        Name of the location for which we want to get an image.
    Returns
    -------
    path:
        The path where the picture is stored.
    """
    images_path = os.path.join(get_root_dir(), "Data\Images")

    #print(images_path)
    
    path = os.path.join(images_path, location_name)

    data_uri = open(path, 'rb').read().encode('base64').replace('\n', '')
    img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)

    
    if (path == (images_path + "/ ")): 
        print("nope")
        return ""
    else: 
        print(img_tag)
        return img_tag

#----------------------------


username = 'optipark'  # Username for the API
password = 'Dyb1yoTU4TG8'  # Password for the API

path_to_urls = get_path_to_csv("Urls.json")  # Path to the json file with the API access links
path_to_csv = get_path_to_csv("Location_Data.csv")  # Path to the csv file containing the location data
path_to_characteristics = get_path_to_csv("Characteristics.csv")  # Path to the csv file containing the characteristics of the locations
path_to_occupancy = get_path_to_csv("Occupancy.csv") # Path to the csv file containing the occupancies of the locations



# --- General functions --- #

def add_location(dic: pd.DataFrame, url:str) -> None:
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
        If the characteristics lat and lon of an location does not exist.
        If the given dic is not from the type dictionary
    """

    check_url(url)  # Check if the url is valid

    if not type(dic) == dict:  # If the dictionary is not a dictionary
        raise Exception('The given dictionary is not a dictionary')  # Raise an exception

    location = dic['location']  # Get the location from the dictionary

    if not check_location_exists(location):  # If the location does not exist yet
        # --- Add the location and its api-access to the Urls.json file --- #
        add_url_to_json(location, url)  # Add the link to the json file

        # --- Append the location with its characteristics to the csv file --- #
        with open(path_to_characteristics, 'a', newline='', encoding='utf-8-sig') as characteristics_file:  # Open the csv file

            writer = csv.writer(characteristics_file, delimiter=',')  # Create a csv writer

            try:
                lat, lon = get_lat_lon_from_url(url)  # Get the latitude and longitude from the url
            except Exception as e:
                lat, lon = 0, 0  # Set the latitude and longitude to None

            writer.writerow([location, lat, lon]
            + list(dic.values())[1:])  # Write the location
            # and its characteristics

            characteristics_file.close()  # Close the file

        # --- Append the location to the csv file containing the occupancies --- #
        add_location_to_occ_csv(location)  # Add the location to the csv file containing the occupancies

    else:  # If the location already exists
        raise Exception('The location {} already exists'.format(location))  # Raise an exception


def check_url(url: str) -> bool:
    """
    This function checks if the url is valid.

    Parameters
    ----------
    url : str
        The url that should be checked.

    Returns
    -------
    valid : bool
        Boolean indicating if the url is valid.

    Raises
    ------
    Exception
        If the url is not a string.
        If the url is not a valid URL.
    """

    if not type(url) == str:  # If the url is not a string
        raise Exception('The given url is not a string')  # Raise an exception

    if not validators.url(url):
        raise Exception(f'The url {url} is not valid')  # Raise an exception


def remove_location(location: str) -> None:
    """
    This function removes the location from the json file and the csv file.

    Parameters
    ----------
    location : str
        The location that should be removed.

    Raises
    ------
    Exception
        If the location is not a string.
        If the location does not exist.
    """

    if not type(location) == str:  # If the location is not a string
        raise Exception('The given location is not a string')  # Raise an exception

    if check_location_exists(location):  # If the location exists
        remove_location_from_json(location)  # Remove the location from the json file

        remove_location_from_csv(location)  # Remove the location from the csv file

        remove_location_from_occ_csv(location)  # Remove the location from the csv file containing the occupancies
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

    Raises
    ------
    Exception
        If the location is not a string.
    """

    if not type(location) == str:  # If the location is not a string
        raise Exception('The given location is not a string')  # Raise an exception

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

    Raises
    ------
    Exception
        If the location is not a string.
        If the location does not exist.
    """

    if not type(location) == str:  # If the location is not a string
        raise Exception('The given location is not a string')  # Raise an exception

    if not check_location_exists(location):  # If the location does not exist
        raise Exception('The location {} does not exist'.format(location))  # Raise an exception

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

    Raises
    ------
    Exception
        If the location is not a string.
        If the URL is not a string.
        If the location does not exist.
    """

    if not type(location) == str:# If the location is not a string
        raise Exception('The given location is not a string')  # Raise an exception

    if not type(url) == str: # If the URL is not a string
        raise Exception('The given url is not a string') # Raise an exception

    if not check_location_exists(location):  # If the location does not exist
        raise Exception('The location {} does not exist'.format(location))  # Raise an exception

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

    Raises
    ------
    Exception
        If the location is not a string.
        If the URL is not a string.
    """

    if not type(location) == str:  # If the location is not a string
        raise Exception('The given location is not a string')  # Raise an exception

    if not type(url) == str:  # If the url is not a string
        raise Exception('The given url is not a string')  # Raise an exception

    with open(get_path_to_csv("Urls.json"), 'r') as f:  # Open the json file with the information about the locations
        content = json.load(f)  # Load the content of the json file

    content[location] = url  # Add the link for the location

    with open(get_path_to_csv("Urls.json"), 'w') as f:  # Open the json file with the information about the locations
        json.dump(content, f, indent=4)  # Write the new content to the json file


def get_url_from_json(location: str) -> str:
    """
    This function returns the url for the given location.

    Parameters
    ----------
    location : str
        The location for which the url should be returned.

    Returns
    -------
    url : str
        The url for the given location.

    Raises
    ------
    Exception
        If the location is not a string.
        If the location does not exist.
    """

    if not type(location) == str:  # If the location is not a string
        raise Exception('The given location is not a string')  # Raise an exception

    if not check_location_exists(location):  # If the location does not exist
        raise Exception('The location {} does not exist'.format(location))  # Raise an exception

    with open(path_to_urls, 'r') as f:  # Open the json file with the information about the locations
        content = json.load(f)  # Load the content of the json file

    return content[location]  # Return the url for the given location


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



def update_characteristics_in_csv(dic:pd.DataFrame) -> None:
    """
    This function updates the characteristics of the location in the csv file.

    Parameters
    ----------
    dic : dict
        Dictionary containing the new characteristics of the location.
    """

    location = dic[0]#identify which location should be modifed

    dic.pop(0)# Deleting the location to avoid the problem of duplication of the location in the CSV

    with open(get_path_to_csv("Characteristics.csv"), 'r',encoding='utf-8-sig') as f:  # Open the csv file
        reader = csv.reader(f)  # Create a csv reader
        lines = list(reader)  # Read the csv file

    with open(get_path_to_csv("Characteristics.csv"), 'w', newline='',encoding='utf-8-sig') as f:  # Open the csv file
        writer = csv.writer(f)  # Create a csv writer

        for line in lines:  # Iterate over the lines
            if line[0] == location:  # If the location is the location that should be updated
                writer.writerow([location, line[1], line[2]] + dic)  # Write the new characteristics to
                # the csv file
            else:  # If the location is not the location that should be updated
                writer.writerow(line)  # Write the line to the csv file


# --- Functions for the Occupancy.csv file --- #

# TODO: Add a function that updates the occupancies of all locations
def update_occupancies():
    """
    This function updates the occupancies of all locations given in the Urls.json file.
    """

    """in this branch no occupancies are read"""
    return

    urls = []
    occupancies = []
    with open(path_to_urls, 'r') as f:  # Open the json file with the information about the locations
        content = json.load(f)  # Load the content of the json file
        for location in content:
            urls.append(content[location])#append the urls of the locations  of the json file
        f.close()

    import time# importing the libary time

    for url in urls:  #iterating through the all arrays
        start_time = time.time()  #saving the starting time(current time)
        occupancies.append(get_occupancy_from_url(url))  #getting the occupancy of the location by using the url of the location
        print("--- %s seconds ---" % (time.time() - start_time))  #printing the time needed to get the occupancy informations

    with open(path_to_occupancy, 'a', newline='\n') as f:  # Open the csv file
        writer = csv.writer(f)  # Create a csv writer
        writer.writerow([datetime.now()] + occupancies)  # Write the new row to the csv file
        f.close()


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

    Raises
    ------
    Exception
        If the location does not exist.
    """

    if not check_location_exists(location):  # If the location does not exist
        raise Exception('The location {} does not exist'.format(location))  # Raise an exception

    all_locations = []
    with open(path_to_urls, 'r') as f:  # Open the json file with the information about the locations
        content = json.load(f)  # Load the content of the json file
        for loc in content:
            all_locations.append(loc)
        url = content[location]  # Get the url for the location

    tendency, occupancy = get_occupancy_from_url(url)  # Get the occupancy from the url

    with open(path_to_occupancy, 'r') as f:  # Open the csv file
        reader = csv.reader(f)  # Create a csv reader
        lines = list(reader)  # Read the csv file

    last_row = lines[-1][1:]  # Get the last row of the csv file (without the time stamp)

    new_row = [datetime.now()]  # Create a new row with the current time stamp

    for i in range(len(all_locations)):  #iterating through all locations
        if all_locations[i] == location:  #if the given location was found (already exist)
            new_row.append((tendency, occupancy)) #adding th tendency and the occupancy of the location
        else:
            new_row.append(last_row[i])#for all other location we are storing the value of the last call

    with open(path_to_occupancy, 'a', newline='\n') as f:  # Open the csv file
        writer = csv.writer(f)  # Create a csv writer
        writer.writerow(new_row)  # Write the new row to the csv file
        f.close()


def add_location_to_occ_csv(location: str) -> None:
    """
    This function adds the location to the occupancy csv file. Note that the location is added to the first row of the
    csv file. For every timestamp already existing in the csv file, the occupancy of the location is set to no value.

    Parameters
    ----------
    location : str
        The location that should be added.
    """

    with open(path_to_occupancy, 'r') as f:  # Open the csv file
        reader = csv.reader(f)  # Create a csv reader
        lines = list(reader)  # Read the csv file

    lines[0].append(location)  # Add the location to the first row
    for i in range(1, len(lines)):  # Iterate over the rows
        lines[i].append('None')  # Add an empty value to the row

    with open(path_to_occupancy, 'w', newline='\n') as f:  # Open the csv file
        writer = csv.writer(f)  # Create a csv writer
        writer.writerows(lines)  # Write the new rows to the csv file
        f.close()


def remove_location_from_occ_csv(location: str) -> None:
    """
    This function removes the location from the occupancy csv file.

    Parameters
    ----------
    location : str
        The location that should be removed.
    """

    with open(path_to_occupancy, 'r') as f: # opening the occupancy file
        reader = csv.reader(f)  # creating a reader for the file
        lines = list(reader)  #storing the informations of the file in a list

    for i in range(len(lines[0])):  #iterating through this list of occupancies
        if lines[0][i] == location:  #if the location was found which should be deleted
            index = i
            break

    for line in lines:  # deleting the row
        del line[index]

    with open(path_to_occupancy, 'w', newline='\n') as f: # opening the occupancy file
        writer = csv.writer(f) # creating a writer for the file
        writer.writerows(lines) #writing all lines which are left in the file
        f.close()


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


def get_occupancy_from_url(url: str) -> str:
    """
    This function returns the occupancy of the location given in the API.

    Parameters
    ----------
    url : str
        The url for the API access.

    Returns
    -------
    occupancy : str
        The occupancy of the location.
    """

    data = get_dict_from_url(url)  # Access the API and get the dictionary with the information

    tendency, occupancy = data['occupancy_tendency:de'], data['occupancy_label:de']  # Get the occupancy of the location

    return tendency, occupancy  # Return the occupancy of the location


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

    response = get_response_from_url(url)  # Send a request to the url and get the response

    data = response.json()  # Extract the json data from the response

    return data[0]  # Return the first element of the list (that is, the dictionary)


def get_response_from_url(url: str) -> Response:
    """
    This function sends a request to the url and returns the response. The response is defined as the content saved in the IRL.

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

    return requests.get(url, auth=(username, password))  # Return the response
