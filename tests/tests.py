from add_test import *
from base_test import *
from production_test import *

test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(ServiceOperationsTest))
test_suite.addTest(unittest.makeSuite(AddListsTest))

test_suite.addTest(unittest.makeSuite(MergeableTest))
test_suite.addTest(unittest.makeSuite(MergeTest))
test_suite.addTest(unittest.makeSuite(AutnumRangeMergeTest))
test_suite.addTest(unittest.makeSuite(AutnumRangeFittestTest))
test_suite.addTest(unittest.makeSuite(AutnumRangeComplementTest))
test_suite.addTest(unittest.makeSuite(AutnumRangeListMergeTest))
test_suite.addTest(unittest.makeSuite(ValidationTest))
test_suite.addTest(unittest.makeSuite(LibsTest))

test_suite.addTest(unittest.makeSuite(FinalTest))

runner=unittest.TextTestRunner()

runner.run(test_suite)