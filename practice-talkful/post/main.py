from threading import Lock, Thread

from audio.api import start_record, stop_stream
from audio.types import StreamHandle
from asr.api import load_model, recognize, unload_model
from asr.types import AsrModelHandle
from config import AppConfig, load_config, write_config
from eventloop import eventloop
from shortcut.api import register_shortcut, unregister_shortcut
from shortcut.types import ShortcutEvent
from text_inject.api import inject_text
from web_console import create_web_console_server

active_stream: StreamHandle | None = None
recorded_samples: list[float] = []
asr_model: AsrModelHandle | None = None
current_config: AppConfig | None = None
config_lock = Lock()


def handle_shortcut(event: ShortcutEvent):
    global active_stream, recorded_samples, asr_model

    with config_lock:
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

def get_config() -> AppConfig:
    with config_lock:
        if current_config is None:
            raise RuntimeError("Config is not initialized")
        return current_config

def apply_config(config: AppConfig) -> None:
    global asr_model, current_config
    if not config.model_path.strip():
        raise ValueError("model_path must be a non-empty string")

    with config_lock:
        old_config = current_config
        old_model = asr_model

        new_model = load_model(config.model_path)
        if old_model is not None:
            unload_model(old_model)

        if old_config is not None:
            unregister_shortcut(old_config.shortcut_key)
        register_shortcut(config.shortcut_key, handle_shortcut)

        current_config = config
        asr_model = new_model
        write_config(config)

def main():

    apply_config(load_config())

    # web console thread
    server = create_web_console_server(get_config=get_config, apply_config=apply_config, port=get_config().web_port)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    eventloop()

if __name__ == '__main__':
    main()
