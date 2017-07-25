import sys, getopt
import json
import requests

argv = sys.argv[1:]

print "Fetching remote files..."
outputdir = 'resources'

try:
    opts, args = getopt.getopt(argv, ":o:", ["odir="])
except getopt.GetoptError:
    print 'fetch_files.py -o <outputdir>'
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-o", "--odir"):
        outputdir = arg

# Script
objects_file = "resources/objects.json"
json_ = open(objects_file, mode='r').read()
objects_ = json.loads(json_)["objects"]
for o in objects_:
    url = o['url']
    response = requests.get(url)

    if response.status_code != 200:
        continue

    response = json.loads(response.text)

    filename = o['filename']
    o_dump = json.dumps(
        response,
        indent=4,
        sort_keys=True
    )
    file = open(filename, 'w')
    file.write(o_dump)
    file.close()
