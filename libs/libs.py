from __future__ import print_function

import copy
from collections import defaultdict

# from libs.exceptions.exceptions import *

NETWORK = "network"
AUTNUM = "autnum"
NOKIND = ""
VALID_KINDS = [NOKIND, NETWORK, AUTNUM]
MANDATORY_KEYS = ["url", "filename", "precedence", "kind", "python_object"]


def eprint(*args, **kwargs):
    # print(*args, file=sys.stderr, **kwargs)
    pass


class ResourceObject(dict):
    def __init__(self, **kwargs):
        super(ResourceObject, self).__init__(**kwargs)

        self["url"] = ""
        self["filename"] = ""
        self["precedence"] = 0
        self["kind"] = NOKIND
        self["python_object"] = {}

    def add_python_object(self, python_object):
        self["python_object"] = python_object


class AutnumRangeList(list):
    def total_count(self):
        count = 0
        for asn_range in self:
            count += asn_range.end - asn_range.start + 1
        return count


class AutnumRange():
    start = 0
    end = 0

    def __init_from_start_end__(self, start, end):
        self.start = start
        self.end = end

    def __init_from_string__(self, string):
        if type(string) is not str:
            msg = "Argument not of type str: %s" % string
            eprint(msg)
            # raise BadArgumentException(msg)

        if "-" in string:
            self.start = int(string.split("-")[0])
            self.end = int(string.split("-")[1])
        else:
            self.start = int(string)
            self.end = self.start

    def __init__(self, *args, **kwargs):
        if "string" in kwargs.keys():
            return self.__init_from_string__(kwargs["string"])
        else:
            return self.__init_from_start_end__(args[0], args[1])

    def __str__(self):
        if self.start == self.end:
            return "%s" % self.start

        if self.start != self.end:
            return "%s-%s" % (self.start, self.end)

    def is_within(self, another_greater_autnumrange):
        if type(another_greater_autnumrange) is not type(self):
            eprint("Not an Autnum Range passed")
            return False

        return another_greater_autnumrange.start <= self.start <= another_greater_autnumrange.end and \
               another_greater_autnumrange.start <= self.end <= another_greater_autnumrange.end

    def minus(self, another_inner_autnumrange):
        """
        :param another_inner_autnumrange:
        :return: an AutnumRange list
        """
        if type(another_inner_autnumrange) is not type(self):
            eprint("Not an Autnum Range passed")
            return [self]

        if not another_inner_autnumrange.is_within(self):
            eprint("Not an Inner Autnum Range passed")
            return [self]

        res = []

        if self.start < another_inner_autnumrange.start:
            res.append(AutnumRange(self.start, another_inner_autnumrange.start - 1))

        if self.end > another_inner_autnumrange.end:
            res.append(AutnumRange(another_inner_autnumrange.end + 1, self.end))

        return res

    def get_fittest(self, _list):
        """
        :param _list: AutnumRange list of candidates
        :return: First candidate containing self from _list
        """

        for l in _list:
            if self.is_within(l):
                return l
        return None

    def has_fittest(self, _list):
        """
        :param _list: AutnumRange list of candidates
        :return: First candidate containing self from _list
        """

        return self.get_fittest(_list) is not None

    def get_complement(self, _list):
        """
        :param _list:
        :return: All _list AutnumRange elements, except self
        """

        remove = self.get_fittest(_list)
        _list.remove(remove)

        if len(_list) > 0:
            return _list

        return None

    def minus_list(self, _list):
        res = [self]
        for l in _list:

            fittest = l.get_fittest(res)
            if fittest is None:
                continue

            complement = fittest.get_complement(res)
            res = fittest.minus(l)
            if complement is not None:
                for c in complement:
                    res.append(c)
        return sorted(res, key=str)


def validate_resourceobject(_object):
    """
    :param _object: whole python object with metadata
    :return:
    """

    if not isinstance(_object, ResourceObject) and type(_object) is not dict:
        eprint("Object type is not dict")
        return False

    if not set(MANDATORY_KEYS).issubset(set(_object.keys())):
        eprint("Object has not all mandatory keys")
        return False

    kind_ = _object["kind"]
    if kind_ not in VALID_KINDS:
        eprint("Object has not got a valid kind (%s)" % kind_)
        return False

    if not type(_object["python_object"]) is dict:
        eprint("Object has not got a valid python object inside")
        return False

    if not type(_object["precedence"]) is int:
        eprint("Object has not got a valid precedence")
        return False

    return True


def same_keys(object1, object2):
    if "kind" not in object1.keys() or "kind" not in object2.keys():
        return False

    if object1["kind"] != object2["kind"]:
        return False

    # At lest one set of keys is included in the other
    s1 = set(object1.keys())
    s2 = set(object2.keys())
    return s1.issubset(s2) or s1.issuperset(s2)


def string_list_minus_string_list(asns1, asns2):
    """
    :param asns1: low-precedence string list
    :param asns2: high-precedence string list
    :return: asns1 list minus asns2 string list
    """

    if type(asns1) is not list or type(asns2) is not list:
        return asns2

    res = []

    autnumranges1 = [AutnumRange(string=str(s)) for s in asns1]
    autnumranges2 = [AutnumRange(string=str(s)) for s in asns2]

    for autnumrange1 in autnumranges1:
        res += autnumrange1.minus_list(autnumranges2)

    return [str(r) for r in res]


def get_endpoint_index(_list):
    """
    :param _list:
    :return: the endpoint list and index where it is
    """

    _list = _list[0]  # CHANGE Remove this line
    if len(_list) != 2:
        return None

    for i, l in enumerate(_list):
        for j, ll in enumerate(l):
            if "http" in ll or "https" in ll:
                return i
    return None


def get_endpoint_list(_list):
    """
    :param _list: [["service-1", "service-2"], ["http://my-service-endpoint.net"]]
    :return: the index in which the service endpoint list is at
    """
    index = get_endpoint_index(_list)
    if index is None:
        return None

    return _list[0][index]  # CHANGE: _list[0] --> _list


def get_service_index(_list):
    index = get_endpoint_index(_list)
    if index is None:
        return None
    endpoint = index
    return 0 if endpoint == 1 else 1


def get_service_list(_list):
    index = get_service_index(_list)
    if index is None:
        return None

    # TODO: Assume multiple services in the same *whole_object*
    return _list[0][index]


def substract(whole_object1, whole_object2):
    """
        :param whole_object1:
        :param whole_object2:
        :return:
    """
    whole_object1_copy = copy.deepcopy(whole_object1)
    whole_object2_copy = copy.deepcopy(whole_object2)
    object1 = whole_object1_copy["python_object"]
    object2 = whole_object2_copy["python_object"]

    if not same_keys(whole_object1, whole_object2):
        eprint("Not same_keys objects")
        return defaultdict(str)

    kind = whole_object1["kind"]

    # We should iterate only though the shortest set of keys
    if len(object1.keys()) < len(object2.keys()):
        common = object1
        longest = object2
    else:
        common = object2
        longest = object1

    # Merge shallow keys first
    for k in common.keys():
        c = common[k]
        l = longest[k]

        if k == "services":
            if kind == NETWORK:
                longest[k] = c + l
            elif kind == AUTNUM:
                lowest_to_highest = sorted([whole_object1_copy, whole_object2_copy], key=lambda x: x["precedence"])
                lowest = lowest_to_highest[0]
                highest = lowest_to_highest[1]

                lowest_service_list = get_service_list(lowest["python_object"][k])
                highest_service_list = get_service_list(highest["python_object"][k])
                new_parent_service = string_list_minus_string_list(
                    lowest_service_list,
                    highest_service_list
                )
                longest[k][0][get_service_index(longest[k])] = new_parent_service
            else:
                longest[k] = c + l

    whole_object1_copy["python_object"] = longest
    return whole_object1_copy


def add(whole_object1, whole_object2):
    """
    :param whole_object1:
    :param whole_object2:
    :return: A simple list, the result of whole_object1 services list and whole_object2
            services list concatenated
    """

    object1_service_list = get_service_list(whole_object1["python_object"]["services"])
    object2_service_list = get_service_list(whole_object2["python_object"]["services"])

    addition = object1_service_list + object2_service_list
    return addition


def add_services(whole_object1, whole_object2):
    """
    :param whole_object1:
    :param whole_object2:
    :return: whole_object2 services copied into whole_object1
    """

    whole_object1_copy = copy.deepcopy(whole_object1)
    whole_object2_copy = copy.deepcopy(whole_object2)

    for service in whole_object2_copy["python_object"]["services"]:
        whole_object1_copy["python_object"]["services"].append(service)

    return whole_object1_copy


def remove_service_by_endpoint(whole_object, endpoint=""):
    """
    :param whole_object: a whole object with multiple services within
    :param endpoint:
    :return:
    """
    whole_object_copy = copy.deepcopy(whole_object)
    res = []
    for service in whole_object_copy["python_object"]["services"]:
        service = [service]  # REMOVE this line after refactor
        endpoint_list = get_endpoint_list(service)
        if endpoint not in endpoint_list:
            res.append(service[0])  # CHANGE service[0] --> service

    whole_object_copy["python_object"]["services"] = res
    return whole_object_copy


def services_have_endpoint(whole_object, endpoint=""):
    """
    :param whole_object: a whole object with multiple services within
    :param endpoint:
    :return:
    """
    for service in whole_object["python_object"]["services"]:
        service = [service]  # REMOVE this line after refactor
        endpoint_list = get_endpoint_list(service)
        if endpoint in endpoint_list:
            return True

    return False


def services_have_endpoints(whole_object, endpoints=[]):
    """
    :param whole_object: a whole object with multiple services within
    :param endpoint:
    :return:
    """

    for endpoint in endpoints:
        if not services_have_endpoint(whole_object, endpoint=endpoint):
            return False
    return True