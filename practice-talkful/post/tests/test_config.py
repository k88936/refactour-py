import tempfile
import unittest
from pathlib import Path

from config import (
    AppConfig,
    load_config,
    write_config,
)
from shortcut.types import Shortcut


class ConfigFunctionsTest(unittest.TestCase):
    def test_load_config_returns_defaults_when_file_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config = load_config(path=str(Path(temp_dir) / "missing.json"))
            self.assertEqual(config, AppConfig(shortcut_key=Shortcut.F1, model_path="asr_model.txt"))

    def test_load_config_parses_valid_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            config_path.write_text('{"shortcut_key":"F2","model_path":"custom_model.txt"}', encoding="utf-8")

            config = load_config(path=str(config_path))
            self.assertEqual(config, AppConfig(shortcut_key=Shortcut.F2, model_path="custom_model.txt"))

    def test_load_config_rejects_invalid_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            config_path.write_text('{"shortcut_key":', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Invalid JSON"):
                load_config(path=str(config_path))

    def test_load_config_rejects_invalid_shortcut(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            config_path.write_text('{"shortcut_key":"F100","model_path":"custom_model.txt"}', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "unsupported shortcut_key"):
                load_config(path=str(config_path))

    def test_write_config_persists_expected_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            write_config(
                AppConfig(shortcut_key=Shortcut.F3, model_path="saved_model.txt"),
                path=str(config_path),
            )

            self.assertEqual(
                config_path.read_text(encoding="utf-8"),
                '{\n  "shortcut_key": "F3",\n  "model_path": "saved_model.txt"\n}\n',
            )

if __name__ == "__main__":
    unittest.main()
