import unittest
from get_files_libs import *
import copy


class MergeableTest(unittest.TestCase):
    """
        Object with metadata testing
    """

    def testMergeable(self):
        _object = {"python_object": {"a": [1]}, "kind": AUTNUM}
        self.assertTrue(
            mergeable(
                _object,
                _object
            ))

    def testNotMergeable(self):
        _object = {"python_object": {"a": [1]}, "kind": AUTNUM}
        strange_object = {"python_object": {"a": [1]}, "hello": "world"}
        self.assertFalse(
            mergeable(
                _object,
                strange_object
            ))

    def testMergeWithEndpoint1(self):
        self.assertDictEqual(
            object_minus_object(
                {
                    "python_object": {"services": [["1"], ["http://my-rir.net"]]},
                    "precedence": 0,
                    "kind": AUTNUM
                },
                {
                    "python_object": {"services": [["2"], ["http://my-nir.net"]]},
                    "precedence": 1,
                    "kind": AUTNUM
                }
            ),
            {
                "python_object": {"services": [["1"], ["http://my-rir.net"]]},
                "precedence": 0,
                "kind": AUTNUM
            }
        )

    def testMergeWithEndpoint2(self):
        """
            Swapped positions
        :return:
        """
        self.assertDictEqual(
            object_minus_object(
                {
                    "python_object": {"services": [["1"], ["http://my-rir.net"]]},
                    "precedence": 0,
                    "kind": AUTNUM
                },
                {
                    "python_object": {"services": [["http://my-nir.net"], ["2"]]},
                    "precedence": 1,
                    "kind": AUTNUM
                }
            ),
            {
                "python_object": {"services": [["1"], ["http://my-rir.net"]]},
                "precedence": 0,
                "kind": AUTNUM
            }
        )

    def testMergeWithEndpoint3(self):
        """
            Swapped positions
        :return:
        """
        self.assertDictEqual(
            object_minus_object(
                {
                    "python_object": {"services": [["1-10"], ["http://my-rir.net"]]},
                    "precedence": 0,
                    "kind": AUTNUM
                },
                {
                    "python_object": {"services": [["http://my-nir.net"], ["5-7"]]},
                    "precedence": 1,
                    "kind": AUTNUM
                }
            ),
            {
                "python_object": {"services": [["1-4", "8-10"], ["http://my-rir.net"]]},
                "precedence": 0,
                "kind": AUTNUM
            }
        )


class MergeTest(unittest.TestCase):
    def testMergeAutnumsWithin(self):
        self.assertListEqual(
            string_list_minus_string_list(["12-15"], ["13-14"]),
            ["12", "15"]
        )

    def testMergeAutnumsSameStart(self):
        self.assertListEqual(
            string_list_minus_string_list(["12-15"], ["12-14"]),
            ["15"]
        )

    def testMergeAutnumsSameEnd(self):
        self.assertListEqual(
            string_list_minus_string_list(["12-15"], ["13-15"]),
            ["12"]
        )

    def testMergeAutnumsMinusNumber(self):
        self.assertListEqual(
            string_list_minus_string_list(["12-15"], ["15"]),
            ["12-14"]
        )

    def testMergeAutnumsMinusItself(self):
        self.assertListEqual(
            string_list_minus_string_list(["12-15"], ["12-15"]),
            []
        )

    def testMergeAutnumsMultipleParents(self):
        self.assertListEqual(
            string_list_minus_string_list(["12-15", "16-18"], ["12-14"]),
            ["15", "16-18"]
        )

    def testMergeAutnumsMultipleChildren(self):
        self.assertListEqual(
            string_list_minus_string_list(["12-18"], ["13-16", "17-18"]),
            ["12"]
        )

    def testMergeAutnumsMultipleChildrenOutOfBounds(self):
        self.assertListEqual(
            string_list_minus_string_list(["12-18"], ["13-16", "17-18", "20-22"]),
            ["12"]
        )

    def testMergeAutnumsMultipleParentsChildren(self):
        self.assertListEqual(
            string_list_minus_string_list(["12-15"], ["12-15"]),
            []
        )

    def testMergeAutnumsNumberMinusNumber(self):
        self.assertListEqual(
            string_list_minus_string_list(["12"], ["15"]),
            ["12"]
        )

    def testMergeObject(self):
        services1 = [
            [
                ["23202", "264493-264512"],
                ["https://my_rdap.nir.net", "http://my_rdap.nir.net"]
            ]
        ]

        services2 = [
            [
                ["23203", "264493-264512"],
                ["https://my_rdap.nir.net", "http://my_rdap.nir.net"]
            ]
        ]

        services3 = [
            [
                ["23202", "23203", "264493-264512"],
                ["https://my_rdap.nir.net", "http://my_rdap.nir.net"]
            ]
        ]

        ro1 = ResourceObject()
        ro2 = ResourceObject()
        ro3 = ResourceObject()

        ro1.add_python_object(
            {
                "services": services1
            }
        )

        ro2.add_python_object(
            {
                "services": services2
            }
        )

        ro3.add_python_object(
            {
                "services": services3
            }
        )


class AutnumRangeMergeTest(unittest.TestCase):
    """
        Testing the AutnumRange *string_list_minus_string_list* function
    """

    def testMergeAutnumsWithinShort(self):
        self.assertListEqual(
            [str(m) for m in AutnumRange(12, 15).minus(AutnumRange(13, 14))],
            ["12", "15"]
        )

    def testMergeAutnumsWithinLong(self):
        self.assertListEqual(
            [str(m) for m in AutnumRange(0, 100).minus(AutnumRange(13, 14))],
            ["0-12", "15-100"]
        )

    def testMergeAutnumsSameStart(self):
        self.assertListEqual(
            [str(m) for m in AutnumRange(12, 15).minus(AutnumRange(12, 14))],
            ["15"]
        )

    def testMergeAutnumsSameEnd(self):
        self.assertListEqual(
            [str(m) for m in AutnumRange(12, 15).minus(AutnumRange(13, 15))],
            ["12"]
        )

    def testMergeAutnumsMinusNumber(self):
        self.assertListEqual(
            [str(m) for m in AutnumRange(12, 15).minus(AutnumRange(15, 15))],
            ["12-14"]
        )

    def testMergeAutnumsMinusItself(self):
        self.assertListEqual(
            [str(m) for m in AutnumRange(12, 15).minus(AutnumRange(12, 15))],
            []
        )

    def testMergeAutnumsNumberMinusNumberSame(self):
        self.assertListEqual(
            [str(m) for m in AutnumRange(12, 12).minus(AutnumRange(12, 12))],
            []
        )

    def testMergeAutnumsNumberMinusNumberDifferent(self):
        self.assertListEqual(
            [str(m) for m in AutnumRange(12, 12).minus(AutnumRange(13, 13))],
            ["12"]
        )


class AutnumRangeFittestTest(unittest.TestCase):
    """
        Testing the AutnumRange *fittest* function
    """

    def testFittest(self):
        autnumrange = AutnumRange(12, 13)
        self.assertEqual(
            str(autnumrange.get_fittest([AutnumRange(12, 15)])),
            "12-15"
        )

    def testFittestFirstCandidate(self):
        autnumrange = AutnumRange(12, 13)
        self.assertEqual(
            str(autnumrange.get_fittest([AutnumRange(12, 15), AutnumRange(16, 20)])),
            "12-15"
        )

    def testFittestLastCandidate(self):
        autnumrange = AutnumRange(12, 13)
        self.assertEqual(
            str(autnumrange.get_fittest([AutnumRange(16, 20), AutnumRange(12, 15)])),
            "12-15"
        )

    def testFittestVeryLastCandidate(self):
        autnumrange = AutnumRange(12, 13)
        self.assertEqual(
            str(autnumrange.get_fittest([AutnumRange(25, 30), AutnumRange(16, 20), AutnumRange(12, 15)])),
            "12-15"
        )


class AutnumRangeFittestTest(unittest.TestCase):
    """
        Testing the AutnumRange *complement* function
    """

    def testComplement(self):
        autnumrange = AutnumRange(12, 13)
        self.assertEqual(
            [str(c) for c in
             autnumrange.get_complement([AutnumRange(25, 30), AutnumRange(16, 20), AutnumRange(12, 15)])],
            ["25-30", "16-20"]
        )

    def testComplementNumber(self):
        autnumrange = AutnumRange(12, 12)
        self.assertEqual(
            [str(c) for c in
             autnumrange.get_complement([AutnumRange(25, 30), AutnumRange(16, 20), AutnumRange(12, 15)])],
            ["25-30", "16-20"]
        )


class AutnumRangeListMergeTest(unittest.TestCase):
    """
        Testing the AutnumRange (parent) *minus_list* function
    """

    def testMergeAutnumRangeListTrivial(self):
        parent = AutnumRange(12, 15)
        _list = [AutnumRange(13, 14)]

        self.assertListEqual(
            [str(m) for m in parent.minus_list(_list)],
            ["12", "15"]
        )

    def testMergeAutnumRangeList(self):
        parent = AutnumRange(12, 15)
        _list = [AutnumRange(12, 12), AutnumRange(13, 14)]

        self.assertListEqual(
            [str(m) for m in parent.minus_list(_list)],
            ["15"]
        )

    def testMergeAutnumRangeListSameStart(self):
        parent = AutnumRange(12, 15)
        _list = [AutnumRange(12, 12), AutnumRange(14, 14)]

        self.assertListEqual(
            [str(m) for m in parent.minus_list(_list)],
            ["13", "15"]
        )

    def testMergeAutnumRangeListSameEnd(self):
        parent = AutnumRange(12, 15)
        _list = [AutnumRange(13, 13), AutnumRange(15, 15)]

        self.assertListEqual(
            [str(m) for m in parent.minus_list(_list)],
            ["12", "14"]
        )

    def testMergeAutnumRangeListNotInRange(self):
        parent = AutnumRange(12, 15)
        _list = [AutnumRange(16, 16)]

        self.assertListEqual(
            [str(m) for m in parent.minus_list(_list)],
            ["12-15"]
        )


class ValidationTest(unittest.TestCase):
    _object = {
        "url": "http://data.iana.org/rdap/asn.json",
        "filename": "iana.asns.json",
        "precedence": 1,
        "kind": AUTNUM,
        "python_object": {}
    }
    _object = ResourceObject()

    def testValidatePositive(self):
        _object_copy = copy.copy(self._object)

        self.assertTrue(
            validate_object(_object_copy)
        )

    def testValidateKeyNegative(self):
        _object_copy = copy.copy(self._object)
        _object_copy.pop("kind", None)

        self.assertFalse(
            validate_object(_object_copy)
        )

    def testValidateKindNegative(self):
        _object_copy = copy.copy(self._object)
        _object_copy["kind"] = "my_kind"

        self.assertFalse(
            validate_object(_object_copy)
        )

    def testValidatePythonObjectNegative(self):
        _object_copy = copy.copy(self._object)
        _object_copy["python_object"] = ""

        self.assertFalse(
            validate_object(_object_copy)
        )

    def testValidatePrecedenceNegative(self):
        _object_copy = copy.copy(self._object)
        _object_copy["precedence"] = ""

        self.assertFalse(
            validate_object(_object_copy)
        )


class LibsTest(unittest.TestCase):
    def testGetHttpsEndpoint1(self):
        self.assertEqual(
            get_endpoint_index([["1", "2"], ["http://my-service.net"]]),
            1
        )

    def testGetHttpsEndpoint2(self):
        self.assertEqual(
            get_endpoint_index([["http://my-service.net"], ["1", "2"]]),
            0
        )

    def testGetHttpsEndpoint3(self):
        self.assertEqual(
            get_endpoint_index([["http://my-service.net"]]),
            None
        )

    def testGetHttpsEndpoint4(self):
        self.assertEqual(
            get_endpoint_index([[], []]),
            None
        )

    def testGetHttpsEndpoint5(self):
        self.assertEqual(
            get_endpoint_index([]),
            None
        )

    def testGetServiceIndex1(self):
        self.assertEqual(
            get_service_index([["1", "2"], ["http://my-service.net"]]),
            0
        )

    def testGetServiceIndex2(self):
        self.assertEqual(
            get_service_index([["http://my-service.net"], ["1", "2"]]),
            1
        )


def main():
    unittest.main()


if __name__ == '__main__':
    main()
