import ast
import unittest
from pathlib import Path

from test_utils import collect_class_def_from_module

MAIN_SOURCE_PATH = Path(__file__).resolve().parents[1] / "src" / "main.py"
CAR_SOURCE_PATH = Path(__file__).resolve().parents[1] / "src" / "car.py"
DRIVER_SOURCE_PATH = Path(__file__).resolve().parents[1] / "src" / "driver.py"


def collect_import_from_module(module: ast.Module) -> dict[str, str]:
    imports: dict[str, str] = {}
    for node in module.body:
        if isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                imports[imported.name] = node.module
    return imports


class MovingClassesTest(unittest.TestCase):
    main_source_text: str
    car_source_text: str
    driver_source_text: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.main_source_text = MAIN_SOURCE_PATH.read_text(encoding="utf-8")
        cls.car_source_text = CAR_SOURCE_PATH.read_text(encoding="utf-8")
        cls.driver_source_text = DRIVER_SOURCE_PATH.read_text(encoding="utf-8")

    def test_car_class_moved_to_car_file(self):
        main_tree = ast.parse(self.main_source_text)
        car_tree = ast.parse(self.car_source_text)

        assert "Car" not in collect_class_def_from_module(main_tree), (
            "Please, move the Car class to a separate file"
        )
        assert "Car" in collect_class_def_from_module(car_tree), (
            "Please, move the Car class to Car file"
        )

    def test_driver_class_moved_to_driver_file(self):
        main_tree = ast.parse(self.main_source_text)
        driver_tree = ast.parse(self.driver_source_text)

        assert "Driver" not in collect_class_def_from_module(main_tree), (
            "Please, move the Driver class to a separate file"
        )
        assert "Driver" in collect_class_def_from_module(driver_tree), (
            "Please, move the Driver class to Driver file"
        )

    def test_main_uses_split_classes(self):
        main_tree = ast.parse(self.main_source_text)
        imports = collect_import_from_module(main_tree)

        assert imports.get("Car") == "car", (
            "Please, import Car from car.py in main.py"
        )
        assert imports.get("Driver") == "driver", (
            "Please, import Driver from driver.py in main.py"
        )
