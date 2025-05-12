import unittest

testmodules = [
    'test_product_repository',
    'test_user_repository',
    'test_order_repository',
    'test_category_repository'
    ]

suite = unittest.TestSuite()

for t in testmodules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner().run(suite)