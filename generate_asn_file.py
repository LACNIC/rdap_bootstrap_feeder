import sys, getopt
import json
from datetime import datetime
import tzlocal

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


def main(outputdir):
    iana = get_object_by_filename("iana.asn.json")
    iana_minus_rir = remove_service_by_endpoint(iana, endpoint="https://rdap.lacnic.net/rdap/")

    rir = get_object_by_filename("rir.asn.json")
    nirs = get_object_by_filename("nirs.asn.json")
    rir_minus_nirs = substract(rir, nirs)

    except_nirs = add_services(iana_minus_rir, rir_minus_nirs)

    final_object = add_services(except_nirs, nirs)["python_object"]

    final_object['publication'] = datetime.now(tzlocal.get_localzone()).strftime("%Y-%m-%d %H:%M:%S%Z:00")

    # print to stdout
    filename = "%s/final.asn.json" % outputdir
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

    outputdir = 'resources'

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, ":o:", ["odir="])
    except getopt.GetoptError:
        print sys.argv[0], ' -o <outputdir>'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-o", "--odir"):
            outputdir = arg

    print "Output dir: %s" % outputdir

    main(outputdir=outputdir)
