import unittest
from pathlib import Path


class RefactorTest(unittest.TestCase):
    def test_long_function(self):
        line_count = len(Path("main.py").read_text().splitlines())
        if line_count >= 70:
            self.fail(f"why not move config related code to config.py")

    def test_move_code(self):
        line_count = len(Path("config.py").read_text().splitlines())
        if line_count <= 10:
            self.fail(f"why not move config related code to config.py")

    def test_no_bad_variable_names(self):
        content = Path("main.py").read_text()
        for var in ["path1", "exc1"]:
            if var in content:
                self.fail(f"Variable '{var}' should be renamed")

    def test_aigc(self):
        content = Path("main.py").read_text() + Path("config.py").read_text()
        if "klAud" in content:
            self.fail("please review aigc (search for 'klAud' :p)")

if __name__ == '__main__':
    unittest.main()
