import sys, getopt
import json

from libs.libs import *


def get_object_by_filename(filename):
    """
    :param filename:
    :return: whole_object
    """
    for o in objects_:
        if filename in o["filename"]:
            return copy.deepcopy(o)
    return defaultdict(str)


objects_file = "resources/objects.json"
json_ = open(objects_file, mode="r").read()
objects_ = json.loads(json_)["objects"]
# Load the objects_ structure with python objects
# "filename" --> "python_object"
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

    final_object = add_services(except_nirs, nirs)["python_object"]

    # print to stdout
    filename = 'resources/final.asn.json'
    final_object_dump = json.dumps(
        final_object,
        indent=4,
        sort_keys=True
    )
    file = open(filename, 'w')
    file.write(final_object_dump)
    file.close()
    # print(unicode(json.dumps(final_object)))


if __name__ == '__main__':
    print "Generating ASNs file..."
    main()
