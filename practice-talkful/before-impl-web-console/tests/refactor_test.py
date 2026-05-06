import unittest
from pathlib import Path


class RefactorTest(unittest.TestCase):
    def test_long_function(self):
        main_path = Path("main.py")
        line_count = len(main_path.read_text().splitlines())
        self.assertLess(line_count, 70, f"main.py has {line_count} lines, tooooooooooo long")
    def test_move_code(self):
        main_path = Path("config.py")
        line_count = len(main_path.read_text().splitlines())
        self.assertGreater(line_count, 10, f"config.py is nearly empty, why not moving code here ?")

if __name__ == '__main__':
    unittest.main()
