import unittest
from backend.utils.parser import parse_poker_log

class TestParser(unittest.TestCase):
    def test_parse_valid_log(self):
        with open('../data/sample_log.json', 'r') as file:
            hands = parse_poker_log(file)
            self.assertEqual(len(hands), 1)

if __name__ == '__main__':
    unittest.main()
