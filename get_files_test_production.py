import unittest
from get_files_libs import *
from get_files import get_object_by_filename  # REMOVE: Try to remove this import
import json

objects_file = "objects.json"
json_ = open(objects_file, mode="r").read()
objects_ = json.loads(json_)["objects"]
for o in objects_:
    text = open(o["filename"], mode="r").read()
    python_o = json.loads(text)
    o["python_object"] = python_o


class FinalTest(unittest.TestCase):
    def testGetEndpointIndex1(self):
        """

        :return:
        """
        for o in objects_:
            self.assertNotEqual(
                get_endpoint_index(o["python_object"]["services"]),
                None
            )

    def testMergeable(self):
        """
            Test thay all have an endpoint
        :return:
        """
        for o in objects_:
            self.assertNotEqual(
                get_endpoint_index(o["python_object"]["services"]),
                None
            )

    def testDisjoint(self):
        """
            No merge result has parents in NIRs resources
        :return:
        """

        rir = get_object_by_filename("rir.asn.json")
        nirs = get_object_by_filename("nirs.asn.json")
        merge_result = object_minus_object(
            rir,
            nirs
        )

        autnumranges = []
        for asn_res in get_service_list(merge_result["python_object"]["services"]):
            autnumrange_res = AutnumRange(string=asn_res)
            autnumranges.append(autnumrange_res)
        for n in get_service_list(nirs["python_object"]["services"]):
            self.assertEqual(
                AutnumRange(string=str(n)).has_fittest(autnumranges),
                False
            )

    def testFullyJoint(self):
        """
            All merge results have parents in RIR resources
        :return:
        """

        rir = get_object_by_filename("rir.asn.json")
        nirs = get_object_by_filename("nirs.asn.json")
        merge_result = object_minus_object(
            rir,
            nirs
        )

        autnumranges = []
        for asn_res in get_service_list(merge_result["python_object"]["services"]):
            autnumrange_res = AutnumRange(string=asn_res)
            autnumranges.append(autnumrange_res)

        for n in get_service_list(rir["python_object"]["services"]):
            self.assertEqual(
                AutnumRange(string=str(n)).has_fittest(autnumranges),
                True
            )


def main():
    unittest.main()


if __name__ == '__main__':
    main()
