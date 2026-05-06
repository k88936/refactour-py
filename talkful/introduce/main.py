from audio.api import start_record, stop_stream
from audio.types import StreamHandle
from asr.api import load_model, recognize
from asr.types import AsrModelHandle
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
    asr_model = load_model("asr_model.txt")
    register_shortcut(Shortcut.F1, handle_shortcut)
    eventloop()

if __name__ == '__main__':
    main()
