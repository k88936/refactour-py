import ast
import unittest
from pathlib import Path

from test_utils import (
    collect_func_def_from_module,
    collect_method_from_class_in_module,
    has_return_call_in_func_def,
    has_variable_assignment_in_func_def,
)

SOURCE_PATH = Path(__file__).resolve().parents[1] / "src" / "task.py"

class InliningTest(unittest.TestCase):
    source_text: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.source_text = SOURCE_PATH.read_text(encoding="utf-8")

    def test_deleted_variables_and_methods(self):
        tree = ast.parse(self.source_text)
        functions = collect_func_def_from_module(tree)
        target = functions.get("calculate_total_price")

        assert target is not None, "Expected calculate_total_price function to be present."
        assert not has_variable_assignment_in_func_def(target, "total_price"), (
            "Please, identify unnecessary variables"
        )

    def test_expression_call_is_replaced_by_its_body(self):
        tree = ast.parse(self.source_text)
        functions = collect_func_def_from_module(tree)
        target = functions.get("calculate_total_price")

        assert target is not None, "Expected calculate_total_price function to be present."
        assert has_return_call_in_func_def(
            target,
            called_name="sum",
            first_arg_name="product_price",
        ), (
            "Please, replace method or variable call by its body - sum(product_price)"
        )
        assert has_path_write_text_call_in_func_def(
            target,
            file_name="Exception.txt",
        ), (
            "Please, replace method or variable call by its body - "
            "Path(\"Exception.txt\").write_text(str(error), encoding=\"utf-8\")"
        )


def has_path_write_text_call_in_func_def(
    function_node: ast.FunctionDef,
    file_name: str,
) -> bool:
    for node in ast.walk(function_node):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr != "write_text":
                continue
            receiver = node.func.value
            if isinstance(receiver, ast.Call) and isinstance(receiver.func, ast.Name):
                if receiver.func.id == "Path" and len(receiver.args) == 1:
                    file_arg = receiver.args[0]
                    if isinstance(file_arg, ast.Constant) and file_arg.value == file_name:
                        return True
    return False
