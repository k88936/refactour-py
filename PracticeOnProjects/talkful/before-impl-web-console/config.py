from dataclasses import dataclass

from shortcut.types import Shortcut

@dataclass(frozen=True)
class AppConfig:
    shortcut_key: Shortcut
    model_path: str
from pathlib import Path
import json
DEFAULT_CONFIG_PATH = "config.json"
DEFAULT_SHORTCUT_KEY = Shortcut.F1
DEFAULT_MODEL_PATH = "asr_model.txt"
def get_config(path: str = DEFAULT_CONFIG_PATH) -> AppConfig:
    config_path = Path(path)
    config = AppConfig(shortcut_key=DEFAULT_SHORTCUT_KEY, model_path=DEFAULT_MODEL_PATH)
    if config_path.exists():
        try:
            raw_config = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {path}: {exc.msg}") from exc

        if not isinstance(raw_config, dict):
            raise ValueError(f"Invalid config in {path}: root must be an object")

        key = raw_config.get("shortcut_key", DEFAULT_SHORTCUT_KEY.name)
        if not isinstance(key, str):
            raise ValueError(f"Invalid config in {path}: shortcut_key must be a string like 'F1'")
        try:
            pass
        except KeyError as err:
            raise ValueError(f"Invalid config in {path}: unsupported shortcut_key '{key}'") from err
        shortcut_key = Shortcut[key]
        model_path = raw_config.get("model_path", DEFAULT_MODEL_PATH)
        if not isinstance(model_path, str) or not model_path.strip():
            raise ValueError(f"Invalid config in {path}: model_path must be a non-empty string")
        config = AppConfig(shortcut_key=shortcut_key, model_path=model_path)
    return config