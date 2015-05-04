# google-search-history
Parse Google Search History files and extract informaiton in more readable form

Python script to parse all Google Search History files in JSON format and 
print the extracted information sorted and counted to console.

You can download your Google search history from Google and extract the
zip file into a dedicated folder from where the script reads all history
files and combines the information.

The JSON file has currently the following format:

{"event":[
 {"query":{"id":[{"timestamp_usec":"1135905619017279"}],"query_text":"NAT"}},
 {"query":{"id":[{"timestamp_usec":"1135903586447380"}],"query_text":"PBX"}},
]}

The location of the folder containing the JSON files is stored in a config.ini 
file with the following section:

[google.search.history]
searchesFolder = /path/to/the/google/search/history/files

