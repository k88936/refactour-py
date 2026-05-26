import ast
import unittest
from pathlib import Path
SOURCE_PATH = Path(__file__).resolve().parents[1] / "PracticeOnProjects" / "talkful" / "before-impl-web-console"


class RefactorTest(unittest.TestCase):
    source_text: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.main_path = SOURCE_PATH / "main.py"
        cls.config_path = SOURCE_PATH / "config.py"
        cls.main_text = cls.main_path.read_text(encoding="utf-8")
        cls.config_text = cls.config_path.read_text(encoding="utf-8")

    def test_long_function(self):
        line_count = len(self.main_text.splitlines())
        if line_count >= 70:
            self.fail(f"why not move config related code to config.py, since we later need a write config function?")

    def test_move_code(self):
        config_module = ast.parse(self.config_text)
        from test_utils import collect_func_def_from_module
        func_names = collect_func_def_from_module(config_module).keys()

        has_config_func = any("config" in name.lower() for name in func_names)
        if not has_config_func:
            self.fail("why not move config loading code to config.py?")

    def test_no_bad_variable_names(self):
        config_module = ast.parse(self.config_text)
        from test_utils import collect_func_def_from_module
        funcs = collect_func_def_from_module(config_module)

        bad_vars = []
        for func in funcs.values():
            func_args = {arg.arg for arg in func.args.args + getattr(func.args, 'kwonlyargs', [])}
            for node in ast.walk(func):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            if target.id not in func_args and target.id in ["exc1", "path1"]:
                                bad_vars.append(target.id)

        if bad_vars:
            self.fail(f"Variable '{bad_vars[0]}' should be renamed.")

    def test_aigc(self):
        combined_content = self.main_text + "\n" + self.config_text
        if "klAud" in combined_content:
            self.fail("please review aigc (search for 'klAud' :p).")


if __name__ == '__main__':
    unittest.main()