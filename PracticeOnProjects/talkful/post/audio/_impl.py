from typing import Callable

from audio.types import StreamHandle

_next_stream_id = 0
_stream_callbacks: dict[
    StreamHandle,
    tuple[Callable[[list[float]], None], Callable[[], None] | None],
] = {}


def _try_handle_voice_events(raw_event: str) -> bool:
    """
    format: voice {sample:float}
    """
    tokens = raw_event.strip().split()
    if len(tokens) != 2 or tokens[0] != "voice":
        return False

    sample = float(tokens[1])
    if not _stream_callbacks:
        return True

    for on_data, _ in tuple(_stream_callbacks.values()):
        on_data([sample])
    return True


def _start_record(on_data: Callable[[list[float]], None], on_eof: Callable[[], None] | None) -> StreamHandle:
    global _next_stream_id
    handle = StreamHandle(_next_stream_id)
    _next_stream_id += 1
    _stream_callbacks[handle] = (on_data, on_eof)
    return handle


def _stop_stream(handle: StreamHandle):
    callbacks = _stream_callbacks.pop(handle, None)
    if callbacks is None:
        return

    _, on_eof = callbacks
    if on_eof is not None:
        on_eof()
