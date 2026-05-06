import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from shortcut.types import Shortcut


DEFAULT_CONFIG_PATH = "config.json"
DEFAULT_SHORTCUT_KEY = Shortcut.F1
DEFAULT_MODEL_PATH = "asr_model.txt"


@dataclass(frozen=True)
class AppConfig:
    shortcut_key: Shortcut
    model_path: str


def _load_config_content(config_path: Path) -> dict[str, Any]:
    try:
        raw_config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {config_path}: {exc.msg}") from exc

    if not isinstance(raw_config, dict):
        raise ValueError(f"Invalid config in {config_path}: root must be an object")
    return raw_config


def _validate_config(config_data: dict[str, Any], config_path: Path) -> tuple[str, str]:
    shortcut_key = config_data.get("shortcut_key", DEFAULT_SHORTCUT_KEY.name)
    if not isinstance(shortcut_key, str):
        raise ValueError(f"Invalid config in {config_path}: shortcut_key must be a string like 'F1'")
    if shortcut_key not in Shortcut.__members__:
        raise ValueError(f"Invalid config in {config_path}: unsupported shortcut_key '{shortcut_key}'")

    model_path = config_data.get("model_path", DEFAULT_MODEL_PATH)
    if not isinstance(model_path, str) or not model_path.strip():
        raise ValueError(f"Invalid config in {config_path}: model_path must be a non-empty string")
    return shortcut_key, model_path


def load_config(path: str = DEFAULT_CONFIG_PATH) -> AppConfig:
    config_path = Path(path)
    if not config_path.exists():
        return AppConfig(shortcut_key=DEFAULT_SHORTCUT_KEY, model_path=DEFAULT_MODEL_PATH)

    config_data = _load_config_content(config_path)
    shortcut_key, model_path = _validate_config(config_data, config_path)
    return AppConfig(shortcut_key=Shortcut[shortcut_key], model_path=model_path)


def write_config(config: AppConfig, path: str = DEFAULT_CONFIG_PATH) -> None:
    config_path = Path(path)
    config_path.write_text(
        json.dumps(
            {"shortcut_key": config.shortcut_key.name, "model_path": config.model_path},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        )
