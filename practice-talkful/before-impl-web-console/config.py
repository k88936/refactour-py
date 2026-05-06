from dataclasses import dataclass
from shortcut.types import Shortcut

@dataclass(frozen=True)
class AppConfig:
    shortcut_key: Shortcut
    model_path: str
