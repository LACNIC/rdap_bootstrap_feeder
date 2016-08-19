from __future__ import print_function
import unittest
from get_files_libs import *
from get_files import get_object_by_filename  # REMOVE: Try to remove this import
import json
import copy


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

    def testEndpointPresence(self):
        """
            Test they all have an endpoint
            :return:
        """
        for o in objects_:
            self.assertNotEqual(
                get_endpoint_index(o["python_object"]["services"]),
                None
            )

    def testDoesntComeFromNirs(self):
        """
            No substraction result has parents in NIRs resources
            :return:
        """

        rir = get_object_by_filename("rir.asn.json")
        nirs = get_object_by_filename("nirs.asn.json")
        substraction = substract(
            rir,
            nirs
        )

        substraction_autnumranges = []
        for asn_res in get_service_list(substraction["python_object"]["services"]):
            autnumrange_res = AutnumRange(string=asn_res)
            substraction_autnumranges.append(autnumrange_res)

        nir_autnumranges = []
        for nir_res in get_service_list(nirs["python_object"]["services"]):
            nir_autnumranges.append(AutnumRange(string=str(nir_res)))

        for substraction in substraction_autnumranges:
            self.assertFalse(
                substraction.has_fittest(nir_autnumranges)
            )

    def testComesFromRir(self):
        """
            All substraction results have parents in  RIR resources
            :return:
        """

        rir = get_object_by_filename("rir.asn.json")
        nirs = get_object_by_filename("nirs.asn.json")
        substraction = substract(
            rir,
            nirs
        )

        substraction_autnumranges = []
        for asn_res in get_service_list(substraction["python_object"]["services"]):
            autnumrange_res = AutnumRange(string=asn_res)
            substraction_autnumranges.append(autnumrange_res)

        rir_autnumranges = []
        for rir_res in get_service_list(rir["python_object"]["services"]):
            rir_autnumranges.append(AutnumRange(string=str(rir_res)))

        for substraction in substraction_autnumranges:
            self.assertTrue(
                substraction.has_fittest(rir_autnumranges)
            )

    def testRemoveByEndpoint(self):
        iana = get_object_by_filename("iana.asn.json")

        endpoint = "https://rdap.lacnic.net/rdap/"
        iana_minus_endpoint = remove_service_by_endpoint(
            iana,
            endpoint=endpoint  # IMPORTANT check this param on external file
        )

        # Check result hasn't got the endpoint
        self.assertFalse(
            services_have_endpoint(iana_minus_endpoint, endpoint=endpoint)
        )

        # ...but the original object still has it
        self.assertTrue(
            services_have_endpoint(iana, endpoint=endpoint)
        )

    def testCompleteScenario(self):
        """
        Final test
        :return:
        """

        iana = get_object_by_filename("iana.asn.json")
        rir_endpoint = "https://rdap.lacnic.net/rdap/"  # IMPORTANT check this param on external file
        nir_endpoint = "https://rdap.registro.br"  # IMPORTANT check this param on external file

        all_rir_endpoints = [
            rir_endpoint,
            "https://rdap.afrinic.net/rdap/",
            "https://rdap.apnic.net/",
            "https://rdap.arin.net/registry",
            "https://rdap.db.ripe.net/"
        ]

        self.assertTrue(
            services_have_endpoints(iana, endpoints=all_rir_endpoints)
        )

        iana_minus_lacnic = remove_service_by_endpoint(iana, endpoint=rir_endpoint)

        all_rir_minus_lacnic_endpoints = copy.copy(all_rir_endpoints)
        all_rir_minus_lacnic_endpoints.remove(rir_endpoint)
        self.assertTrue(
            services_have_endpoints(iana_minus_lacnic, endpoints=all_rir_minus_lacnic_endpoints)
        )

        rir = get_object_by_filename("rir.asn.json")
        nirs = get_object_by_filename("nirs.asn.json")
        rir_minus_nirs = substract(rir, nirs)
        except_nirs = add_services(iana_minus_lacnic, rir_minus_nirs)
        self.assertTrue(
            services_have_endpoints(except_nirs, endpoints=all_rir_endpoints)
        )

        all_endpoints = copy.copy(all_rir_endpoints)
        all_endpoints.append(nir_endpoint)
        final_object = add_services(except_nirs, nirs)
        self.assertTrue(
            services_have_endpoints(final_object, endpoints=all_endpoints)
        )


objects_ = {}


def main():
    print("Performing production-like tests (they may last a bit)")
    objects_file = "objects.json"
    json_ = open(objects_file, mode="r").read()
    objects_ = json.loads(json_)["objects"]
    for o in objects_:
        text = open(o["filename"], mode="r").read()
        python_o = json.loads(text)
        o["python_object"] = python_o
    unittest.main()


if __name__ == '__main__':
    main()
