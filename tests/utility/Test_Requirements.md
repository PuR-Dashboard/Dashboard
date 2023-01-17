# Necessary tests
## data_functions.py
### add_location(dic, url):

- Test whether function adds location in all files
  - Occupancy.csv
  - Characteristics.csv
  - Url.json
- Test whether exception is raised when url is not a string
- Test whether exception is raised when url is not a valid url
- Test whether exception is raised when dic is not a dictionary
- Test whether exception is raised if the location already exists

### check_location_exists(str):

- Test whether function returns True if location exists
- Test whether function returns False if location does not exist

### remove_location_from_json(str):
- Test whether function removes location from Url.json
- Test whether function raises exception if location does not exist

### update_url_in_json(str, str):
- Test whether function updates url in Url.json
- Test whether function raises exception if location does not exist
- Test whether function raises exception if url is not a string
- Test whether function raises exception if url is not a valid url

### add_url_to_json(str, str):
- Test whether function adds url to Url.json
- Test whether function raises exception if url is not a string
- Test whether function raises exception if url is not a valid url
- Test whether function raises exception if location is not a string

### remove_location_from_csv(str):
- Test whether function removes location from Occupancy.csv

### update_characteristics_in_csv(dic: dict):
- Test whether function updates characteristics in Characteristics.csv
- Test whether function raises exception if dic is not a dictionary

### update_location_occupancy(str):
- Test whether function updates occupancy in Occupancy.csv
- Test whether function raises exception if location does not exist

### add_location_to_occ_csv(str):
- Test whether function adds location to Occupancy.csv
- Test whether function raises exception if location already exists
- Test whether function raises exception if location is not a string

### get_lat_lon_from_url(str):
- Test whether function returns a tuple with latitude and longitude
- Test whether function raises exception if url is not a string
- Test whether function raises exception if url is not a valid url

### get_dict_from_url(str):
- Test whether function returns a dictionary
- Test whether function raises exception if url is not a string
- Test whether function raises exception if url is not a valid url

### get_response_from_url(str):
- Test whether function returns a response
- Test whether function raises exception if url is not a string
- Test whether function raises exception if url is not a valid url
- Test whether function raises exception if response is not 200
