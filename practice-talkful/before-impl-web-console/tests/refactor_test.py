import unittest
from pathlib import Path


class RefactorTest(unittest.TestCase):
    def test_long_function(self):
        main_path = Path("main.py")
        line_count = len(main_path.read_text().splitlines())
        self.assertLessEqual(line_count, 70, f"main.py has {line_count} lines, tooooooooooo long")


if __name__ == '__main__':
    unittest.main()
