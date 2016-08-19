from __future__ import print_function
import unittest
from get_files_libs import *


class AddListsTest(unittest.TestCase):
    def testAdd(self):
        object1 = {"python_object": {"services": [[["1"], ["http://my-rdap.net"]]]}, "kind": AUTNUM}
        addition = add(object1, object1)
        self.assertListEqual(
            sorted(addition),
            sorted(["1", "1"])
        )

    def testAdd2(self):
        object1 = {"python_object": {"services": [[["1"], ["http://my-rdap.net"]]]}, "kind": AUTNUM}
        object2 = {"python_object": {"services": [[["1", "2"], ["http://my-rdap.net"]]]}, "kind": AUTNUM}
        addition = add(object1, object2)
        self.assertListEqual(
            sorted(addition),
            sorted(["1", "1", "2"])
        )


class ServiceOperationsTest(unittest.TestCase):
    def testRemove(self):
        _object = {
            "python_object": {
                "services": [
                    [["1"], ["http://my-service.net"]],
                    [["2"], ["http://my-other-service.net"]]
                ]
            },
            "kind": AUTNUM
        }

        self.assertEqual(
            remove_service_by_endpoint(_object, endpoint="http://my-other-service.net"),
            {
                "python_object": {
                    "services": [
                        [["1"], ["http://my-service.net"]]
                    ]},
                "kind": AUTNUM}
        )

    def testHasEndpoint(self):
        _object = {
            "python_object": {
                "services": [
                    [["1"], ["http://my-service.net"]],
                    [["2"], ["http://my-other-service.net"]]
                ]
            },
            "kind": AUTNUM
        }

        self.assertTrue(
            services_have_endpoint(_object, endpoint="http://my-other-service.net")
        )

    def testHasEndpoints(self):
        _object = {
            "python_object": {
                "services": [
                    [["1"], ["http://my-service.net"]],
                    [["2"], ["http://my-other-service.net"]]
                ]
            },
            "kind": AUTNUM
        }

        self.assertTrue(
            services_have_endpoints(_object, endpoints=[
                                                "http://my-other-service.net",
                                                "http://my-service.net"
                                                    ])
        )

    def testAdd(self):
        endpoint_1 = "http://my-service.net"
        endpoint_2 = "http://my-other-service.net"

        object1 = {
            "python_object": {
                "services": [
                    [["1"], [endpoint_1]],
                ]
            },
            "kind": AUTNUM
        }

        object2 = {
            "python_object": {
                "services": [
                    [["2"], [endpoint_2]]
                ]
            },
            "kind": AUTNUM
        }

        addition = add_services(object1, object2)
        addition_services = addition["python_object"]["services"]

        self.assertEqual(
            len(addition_services),
            2
        )

        self.assertTrue(
            services_have_endpoints(addition, endpoints=[endpoint_1, endpoint_2])
        )



def main():
    unittest.main()


if __name__ == '__main__':
    main()
