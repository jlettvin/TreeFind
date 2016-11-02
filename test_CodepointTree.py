import unittest2

from CodepointTree import ( CodepointTree )

class CodepointTreeTestCase(unittest2.TestCase):

    def setUp(self):
        self.tree = CodepointTree()

    def tearDown(self):
        pass

    def test_0_size(self):
        self.assertEqual(len(self.tree), 0, '0 entries')

    def test_0_fails(self):
        self.assertEqual(self.tree['hello'], False, 'fail request')

    def test_1_size(self):
        self.tree('hello')
        self.assertEqual(len(self.tree), 1, '1 entry')

    def test_1_pass(self):
        self.tree('hello')
        self.assertEqual(self.tree['hello'], set(['hello']), 'pass request')

    def test_1_fail(self):
        self.tree('hello')
        self.assertEqual(self.tree['world'], False, 'fail request')

    def test_2_size(self):
        self.tree(['hello', 'world'])
        self.assertEqual(len(self.tree), 2, '2 entries')

    def test_2_pass(self):
        self.tree(['hello', 'world'])
        self.assertEqual(self.tree['hello'], set(['hello']), 'pass request')
        self.assertEqual(self.tree['world'], set(['world']), 'pass request')

    def test_2_fail(self):
        self.tree(['hello', 'world'])
        self.assertEqual(self.tree['hi'], False, 'fail request')
        self.assertEqual(self.tree['globe'], False, 'fail request')

    def test_2_size_idempotent(self):
        self.tree(['hello', 'world'])
        self.tree('hello')
        self.assertEqual(len(self.tree), 2, '2 entries')

    def test_2_pass_idempotent(self):
        self.tree(['hello', 'world'])
        self.tree('hello')
        self.assertEqual(self.tree['hello'], set(['hello']), 'pass request')
        self.assertEqual(self.tree['world'], set(['world']), 'pass request')

    def test_2_fail_idempotent(self):
        self.tree(['hello', 'world'])
        self.tree('hello')
        self.assertEqual(self.tree['hi'], False, 'fail request')
        self.assertEqual(self.tree['globe'], False, 'fail request')

    def test_canonical(self):
        self.tree('hello')
        self.tree.also('hello', 'helo')
        self.tree.also('hello', 'hllo')
        self.tree.also('hello', 'helo')
        self.assertEqual(self.tree['hello'], set(['hello']), 'pass request')
        self.assertEqual(self.tree['hllo' ], set(['hello']), 'pass request')
        self.assertEqual(self.tree['helo' ], set(['hello']), 'pass request')
