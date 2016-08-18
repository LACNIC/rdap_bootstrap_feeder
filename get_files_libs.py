from __future__ import print_function
from collections import defaultdict
import operator

NETWORK = "network"
AUTNUM = "autnum"
NOKIND = ""
VALID_KINDS = [NOKIND, NETWORK, AUTNUM]
MANDATORY_KEYS = ["url", "filename", "precedence", "kind", "python_object"]

objects = {}


def eprint(*args, **kwargs):
    # print(*args, file=sys.stderr, **kwargs)
    pass


def _print(output):
    print("\r%s" % (output))


class ResourceObject(dict):
    def __init__(self, **kwargs):
        super(ResourceObject, self).__init__(**kwargs)

        self["url"] = ""
        self["filename"] = ""
        self["precedence"] = 0
        self["kind"] = NOKIND
        self["python_object"] = {}

    def __str__(self):
        return str(self.new)

    def add_python_object(self, python_object):
        self["python_object"] = python_object


class AutnumRange():
    start = 0
    end = 0

    def __init__(self, *args, **kwargs):
        if "string" in kwargs.keys():
            return self.__init_from_string__(kwargs["string"])

        return self.__init_from_start_end__(args[0], args[1])

    def __init_from_start_end__(self, start, end):
        self.start = start
        self.end = end

    def __init_from_string__(self, string):
        if type(string) is not str:
            eprint("Argument not of type str")
            return

        if "-" in string:
            self.start = int(string.split("-")[0])
            self.end = int(string.split("-")[1])
        else:
            self.start = int(string)
            self.end = self.start

    def __str__(self):
        if self.start == self.end:
            return "%s" % (self.start)

        if self.start != self.end:
            return "%s-%s" % (self.start, self.end)

    def is_within(self, another_greater_autnumrange):
        if type(another_greater_autnumrange) is not type(self):
            eprint("Not an Autnum Range passed")
            return False

        return another_greater_autnumrange.start <= self.start <= another_greater_autnumrange.end \
               and another_greater_autnumrange.start <= self.end <= another_greater_autnumrange.end

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
            if fittest is None: continue

            complement = fittest.get_complement(res)
            res = fittest.minus(l)
            if complement is not None:
                for c in complement:
                    res.append(c)
        return sorted(res, key=str)


def validate_object(_object):
    if type(_object) is not type(ResourceObject()):
        eprint("Object type is not dict")
        return False

    if not set(MANDATORY_KEYS).issubset(set(_object.keys())):
        eprint("Object has not all mandatory keys")
        return False

    kind_ = _object["kind"]
    if kind_ not in VALID_KINDS:
        eprint("Object has not got a valid kind (%s)" % (kind_))
        return False

    if not type(_object["python_object"]) is dict:
        eprint("Object has not got a valid python object inside")
        return False

    if not type(_object["precedence"]) is int:
        eprint("Object has not got a valid precedence")
        return False

    return True


def mergeable(object1, object2):
    if "kind" not in object1.keys() or "kind" not in object2.keys():
        return False

    if object1["kind"] != object2["kind"]:
        return False

    # At lest one set of keys is included in the other
    s1 = set(object1.keys())
    s2 = set(object2.keys())
    return s1.issubset(s2) or s1.issuperset(s2)


# def merge_autnumranges_list(autnum_ranges1, autnum_ranges2):
#     """
#
#     :param autnum_tanges1: low-precedence AutnumRange list
#     :param autnum_renages2: high-precedence AutnumRange list
#     :return: autnum_ranges1 string_list_minus_string_list autnum_ranges2 AutnumRange list
#     """
#     if type(autnum_ranges1) is not list or type(autnum_ranges2) is not list:
#         return autnum_ranges1
#
#     res = []
#     for autnum_range1 in autnum_ranges1:
#         for autnum_range2 in autnum_ranges2:
#             res += autnum_range1.string_list_minus_string_list(autnum_range2)
#     return res


def string_list_minus_string_list(asns1, asns2):
    """
    :param asns1: low-precedence string list
    :param asns2: high-precedence string list
    :return: asns1 list minus asns2 string list
    """

    if type(asns1) is not list or type(asns2) is not list:
        return asns2

    res = []

    autnumranges1 = [AutnumRange(string=s) for s in asns1]
    autnumranges2 = [AutnumRange(string=s) for s in asns2]

    for autnumrange1 in autnumranges1:
        res += autnumrange1.minus_list(autnumranges2)

    return [str(r) for r in res]


def get_endpoint_index(_list):
    """
    :param _list:
    :return: the endpoint list and index where it is
    """

    _list = _list[0]  # Remove this line
    if len(_list) != 2:
        return None
    # if len(_list) != 1:
    #     return None

    for i, l in enumerate(_list):
        for j, ll in enumerate(l):
            if "http" in ll or "https" in ll:
                return i
    return None


def get_endpoint_list(_list):
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


def object_minus_object(whole_object1, whole_object2):
    """
    :param whole_object1:
    :param whole_object2:
    :return:
    """
    object1 = whole_object1["python_object"]
    object2 = whole_object2["python_object"]

    if not mergeable(whole_object1, whole_object2):
        print("Not mergeable objects")
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

        # if c == l:
        #     continue

        if k == "services":
            if kind == NETWORK:
                longest[k] = c + l
            elif kind == AUTNUM:
                lowest_to_highest = sorted([whole_object1, whole_object2], key=lambda x: x["precedence"])
                lowest = lowest_to_highest[0]
                highest = lowest_to_highest[1]

                # print(get_endpoint_list(lowest["python_object"][k]))
                # print(get_endpoint_list(highest["python_object"][k]))

                lowest_service_list = get_service_list(lowest["python_object"][k])
                highest_service_list = get_service_list(highest["python_object"][k])
                new_parent_service = string_list_minus_string_list(
                    lowest_service_list,
                    highest_service_list
                )
                longest[k][0][get_service_index(longest[k])] = new_parent_service
            else:
                longest[k] = c + l

    whole_object1["python_object"] = longest
    return whole_object1


def merge_multiple(_objects):
    res = _objects[0]
    for o in _objects[1:]:
        res = object_minus_object(res, o)
    return res


def get_object_by_filename(filename):
    for o in objects:
        if o["filename"] == filename:
            return o
    return defaultdict(str)
