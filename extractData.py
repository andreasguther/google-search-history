"""
Reads json files from given directory.  Expects files in the Google Search History JSON format.
{"event":[
 {"query":{"id":[{"timestamp_usec":"1135905619017279"}],"query_text":"NAT"}},
 {"query":{"id":[{"timestamp_usec":"1135903586447380"}],"query_text":"PBX"}},
]}
The folder containing the JSON files is stored in a config.ini file with the section

[google.search.history]
searchesFolder = /path/to/folder

"""
__author__ = 'aguther'
__version__ = "0.2"

import os
import glob
import json
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

searchesFolder = config['google.search.history']['searchesFolder']

searches = {}
searchCounter = 0

for infile in glob.glob(os.path.join(searchesFolder, '*.json')):
    print(infile)
    json_data = open(infile)
    data = json.load(json_data)

    for i in range(0, len(data['event'])):
        search = data['event'][i]['query']['query_text']
        when = datetime.fromtimestamp(int(data['event'][i]['query']['id'][0]['timestamp_usec']) / 1000000)
        day = when.strftime("%Y-%m-%d")
        search = search.lower()
        searchCounter += 1
        if search in searches:
            counter = searches[search]['searched'] + 1
            searches[search]['searched'] = counter
            if day in searches[search]['dates']:
                searches[search]['dates'][day] += 1
            else:
                searches[search]['dates'][day] = 1
        else:
            meta = dict(searched=1, dates={day: 1})
            searches[search] = meta

    json_data.close()

index = 0
for key in sorted(searches.keys()):
    index += 1
    if searches[key]['searched'] > 1:
        dateList = []
        for recordedDate in sorted(searches[key]['dates']):
            recorded = searches[key]['dates'][recordedDate]
            if recorded > 1:
                dateList.append(recordedDate + ' (' + str(searches[key]['dates'][recordedDate]) + 'x)')
            else:
                dateList.append(recordedDate)
        print("%.5d  %s (%sx) - %s" % (index, key, searches[key]['searched'], dateList))
    else:
        print("%.5d  %s (%sx) - %s" % (index, key, searches[key]['searched'], sorted(searches[key]['dates'])))

print("Total number of searches: %d" % searchCounter)

