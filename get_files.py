import json
from get_files_libs import *

merges = [
    # {
    #     "input": ["rir.v4.json", "nirs.v4.json", "iana.v4.json"],
    #     "output": "final.v4.json"
    # },
    # {
    #     "input": ["rir.v6.json", "nirs.v6.json", "iana.v6.json"],
    #     "output": "final.v6.json"
    # },
    {
        "input": ["rir.asn.json", "nirs.asn.json"],
        "output": "final.asn.json"
    }
]


def get_object_by_filename(filename):
    for o in objects_:
        if o["filename"] == filename:
            return o
    return defaultdict(str)


objects_file = "objects.json"
json_ = open(objects_file, mode="r").read()
objects_ = json.loads(json_)["objects"]
for o in objects_:
    # url = o["url"]
    # print("Connecting to %s..." % (url))
    # print("Connected to %s." % (url))
    # response = get(url).text

    response = open(o["filename"], mode="r").read()

    python_o = json.loads(response)
    o["python_object"] = python_o

for m in merges:
    whole_python_objects = []
    for i in m["input"]:
        o = get_object_by_filename(i)
        whole_python_objects.append(o)

    # merge_result = merge_multiple(whole_python_objects)

    rir = get_object_by_filename("rir.asn.json")
    nirs = get_object_by_filename("nirs.asn.json")
    merge_result = object_minus_object(
        rir,
        nirs
    )

    # Print to stdout
    string = json.dumps(merge_result["python_object"])
    print(
        unicode(string)
    )
