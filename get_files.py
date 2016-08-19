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
    """
    :param filename:
    :return: whole_object
    """
    for o in objects_:
        if o["filename"] == filename:
            return copy.deepcopy(o)
    return defaultdict(str)


objects_file = "objects.json"
json_ = open(objects_file, mode="r").read()
objects_ = json.loads(json_)["objects"]
# Load the objects_ structure with python objects
for o in objects_:
    response = open(o["filename"], mode="r").read()
    python_o = json.loads(response)
    o["python_object"] = python_o


def main():
    iana = get_object_by_filename("iana.asn.json")
    iana_minus_rir = remove_service_by_endpoint(iana, endpoint="https://rdap.lacnic.net/rdap/")

    rir = get_object_by_filename("rir.asn.json")
    nirs = get_object_by_filename("nirs.asn.json")
    rir_minus_nirs = substract(rir, nirs)

    except_nirs = add_services(iana_minus_rir, rir_minus_nirs)

    final_object = add_services(except_nirs, nirs)

    print(unicode(final_object["python_object"]))


if __name__ == '__main__':
    main()
