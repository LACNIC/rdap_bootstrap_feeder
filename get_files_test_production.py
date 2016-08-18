import unittest
from get_files_libs import *
import json

objects_file = "objects.json"
json_ = open(objects_file, mode="r").read()
objects_ = json.loads(json_)["objects"]
for o in objects_:

    text = open(o["filename"], mode="r").read()

    python_o = json.loads(text)
    o["python_object"] = python_o

for o in objects_:
    print(
        len(get_service_list(o["python_object"]["services"]))
    )


class FinalTest(unittest.TestCase):
    def testGetEndpointIndex1(self):
        for o in objects_:
            self.assertNotEqual(
                get_endpoint_index(o["python_object"]["services"]),
                None
            )

    def testMergeable(self):
        for o in objects_:
            self.assertNotEqual(
                get_endpoint_index(o["python_object"]["services"]),
                None
            )

    def testDisjoint(self):

        rir = get_object_by_filename("rir.asn.json")
        nirs = get_object_by_filename("nirs.asn.json")
        merge_result = object_minus_object(
            rir,
            nirs
        )

        for o in objects_:
            self.assertNotEqual(
                get_endpoint_index(o["python_object"]["services"]),
                None
            )



def main():
    unittest.main()


if __name__ == '__main__':
    main()
