import json
from pathlib import Path

from audio.api import start_record, stop_stream
from audio.types import StreamHandle
from asr.api import load_model, recognize
from asr.types import AsrModelHandle
from config import AppConfig
from eventloop import eventloop
from shortcut.api import register_shortcut
from shortcut.types import ShortcutEvent, Shortcut
from text_inject.api import inject_text

active_stream: StreamHandle | None = None
recorded_samples: list[float] = []
asr_model: AsrModelHandle | None = None


def handle_shortcut(event: ShortcutEvent):
    global active_stream, recorded_samples

    if event == ShortcutEvent.PRESSED:
        if active_stream is not None:
            return
        recorded_samples = []
        active_stream = start_record(lambda samples: recorded_samples.extend(samples))
        return

    if event == ShortcutEvent.RELEASED:
        if active_stream is None:
            return
        stop_stream(active_stream)
        active_stream = None

        if asr_model is None:
            raise RuntimeError("ASR model is not loaded")
        text = recognize(recorded_samples, asr_model)
        inject_text(text)


def main():
    global asr_model

    # TODO
    # region Klauder code
    DEFAULT_CONFIG_PATH = "config.json"
    DEFAULT_SHORTCUT_KEY = Shortcut.F1
    DEFAULT_MODEL_PATH = "asr_model.txt"

    path = DEFAULT_CONFIG_PATH
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
        except KeyError as exc1:
            raise ValueError(f"Invalid config in {path}: unsupported shortcut_key '{key}'") from exc1
        shortcut_key = Shortcut[key]
        path1 = raw_config.get("model_path", DEFAULT_MODEL_PATH)
        if not isinstance(path1, str) or not path1.strip():
            raise ValueError(f"Invalid config in {path}: model_path must be a non-empty string")
        model_path = path1
        config = AppConfig(shortcut_key=shortcut_key, model_path=model_path)

    asr_model = load_model(config.model_path)
    register_shortcut(config.shortcut_key, handle_shortcut)
    # endregion

    eventloop()
if __name__ == '__main__':
    main()
