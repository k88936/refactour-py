import ast
import unittest
from pathlib import Path

from test_utils import (
    has_module_constant_value_in_module,
    has_variable_assignment_in_func_def,
)

SOURCE_PATH = Path(__file__).resolve().parents[1] / "src" / "task.py"


class ExtractMagicConstantsTest(unittest.TestCase):
    source_text: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.source_text = SOURCE_PATH.read_text(encoding="utf-8")

    def test_extracted_constants_and_variable(self):
        tree = ast.parse(self.source_text)

        assert has_module_constant_value_in_module(tree, 299792458.0), (
            "Please, create constant values for 299792458.0"
        )
        assert has_module_constant_value_in_module(tree, 6.62607015e-34), (
            "Please, create constant values for 6.62607015e-34"
        )

        main_function = next(
            (
                node
                for node in tree.body
                if isinstance(node, ast.FunctionDef) and node.name == "main"
            ),
            None,
        )
        assert main_function is not None, "Expected a main function to be present."
        assert has_variable_assignment_in_func_def(main_function, "wave_length"), (
            "Please, create property for wave_length"
        )
