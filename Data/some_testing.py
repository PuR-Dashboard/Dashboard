import json

with open("Urls.json") as json_file:
    json_decoded = json.load(json_file)

json_decoded['Schmeidelberg'] = 'ADDED_VALUE'

with open("Urls.json", 'w') as json_file:
    json.dump(json_decoded, json_file)


