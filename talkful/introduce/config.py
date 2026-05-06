import json
from dataclasses import dataclass
from pathlib import Path

from shortcut.types import Shortcut

_DEFAULT_CONFIG_PATH = "config.json"
_DEFAULT_SHORTCUT_KEY = Shortcut.F1
_DEFAULT_MODEL_PATH = "asr_model.txt"


@dataclass(frozen=True)
class AppConfig:
    shortcut_key: Shortcut
    model_path: str


def load_app_config(path: str = _DEFAULT_CONFIG_PATH) -> AppConfig:
    """Load app configuration from a JSON file."""
    config_path = Path(path)
    if not config_path.exists():
        return AppConfig(shortcut_key=_DEFAULT_SHORTCUT_KEY, model_path=_DEFAULT_MODEL_PATH)

    try:
        raw_config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc.msg}") from exc

    if not isinstance(raw_config, dict):
        raise ValueError(f"Invalid config in {path}: root must be an object")

    shortcut_key = _parse_shortcut_key(raw_config.get("shortcut_key", _DEFAULT_SHORTCUT_KEY.name), path)
    model_path = _parse_model_path(raw_config.get("model_path", _DEFAULT_MODEL_PATH), path)
    return AppConfig(shortcut_key=shortcut_key, model_path=model_path)


def write_app_config(config: AppConfig, path: str = _DEFAULT_CONFIG_PATH) -> None:
    """Write app configuration to a JSON file."""
    config_path = Path(path)
    if config_path.parent != Path("."):
        config_path.parent.mkdir(parents=True, exist_ok=True)

    raw_config = {
        "shortcut_key": config.shortcut_key.name,
        "model_path": config.model_path,
    }
    config_path.write_text(json.dumps(raw_config, indent=2) + "\n", encoding="utf-8")


def _parse_shortcut_key(shortcut_key: object, config_path: str) -> Shortcut:
    if not isinstance(shortcut_key, str):
        raise ValueError(f"Invalid config in {config_path}: shortcut_key must be a string like 'F1'")
    try:
        return Shortcut[shortcut_key]
    except KeyError as exc:
        raise ValueError(f"Invalid config in {config_path}: unsupported shortcut_key '{shortcut_key}'") from exc


def _parse_model_path(model_path: object, config_path: str) -> str:
    if not isinstance(model_path, str) or not model_path.strip():
        raise ValueError(f"Invalid config in {config_path}: model_path must be a non-empty string")
    return model_path
