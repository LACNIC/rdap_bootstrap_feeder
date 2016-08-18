from requests import get as get
from collections import defaultdict
import json
from get_files_libs import *

endpoint = "http://127.0.0.1:8180/ext"

objects = [
    {
        "url": endpoint + "/rir-space/v4.json?cache=false",
        "filename": "rir.v4.json",
        "precedence": 1,
        "kind": NETWORK,
        "python_object": {}
    },
    {
        "url": endpoint + "/rir-space/v6.json?cache=false",
        "filename": "rir.v6.json",
        "precedence": 1,
        "kind": NETWORK,
        "python_object": {}
    },
    {
        "url": endpoint + "/rir-space/asn.json?cache=false",
        "filename": "rir.asns.json",
        "precedence": 2,
        "kind": AUTNUM,
        "python_object": {}
    },
    {
        "url": endpoint + "/nir-space/v4.json?cache=false",
        "filename": "nirs.v4.json",
        "precedence": 1,
        "kind": NETWORK,
        "python_object": {}
    },
    {
        "url": endpoint + "/nir-space/v6.json?cache=false",
        "filename": "nirs.v6.json",
        "precedence": 1,
        "kind": NETWORK,
        "python_object": {}
    },
    {
        "url": endpoint + "/nir-space/asn.json?cache=false",
        "filename": "nirs.asns.json",
        "precedence": 3,
        "kind": AUTNUM,
        "python_object": {}
    },
    {
        "url": "http://data.iana.org/rdap/ipv4.json",
        "filename": "iana.v4.json",
        "precedence": 1,
        "kind": NETWORK,
        "python_object": {}
    },
    {
        "url": "http://data.iana.org/rdap/ipv6.json",
        "filename": "iana.v6.json",
        "precedence": 1,
        "kind": NETWORK,
        "python_object": {}
    },
    {
        "url": "http://data.iana.org/rdap/asn.json",
        "filename": "iana.asns.json",
        "precedence": 1,
        "kind": AUTNUM,
        "python_object": {}
    }
]

merges = [
    {
        "input": ["rir.v4.json", "nirs.v4.json", "iana.v4.json"],
        "output": "final.v4.json"
    },
    {
        "input": ["rir.v6.json", "nirs.v6.json", "iana.v6.json"],
        "output": "final.v6.json"
    },
    {
        "input": ["nirs.asns.json", "iana.asns.json"],
        "output": "final.asns.json"
    }
]

# new_object = defaultdict(str)  # TODO

for o in objects:
    url = o["url"]
    print("Connecting to %s..." % (url))
    print("Connected to %s." % (url))
    response = get(url).text

    python_o = json.loads(response)
    o["python_object"] = python_o

for m in merges:
    merge_result = merge_multiple([get_object_by_filename(i) for i in m["input"]])
    print("\nWriting merge in %s" % (m["output"]))
    _file = open(m["output"], 'w')
    _file.write(json.dumps(merge_result))
    _file.close()
