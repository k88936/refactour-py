from typing import Callable

from audio._impl import _start_record, _stop_stream
from audio.types import StreamHandle


def start_record(
    on_data: Callable[[list[float]], None],
    on_eof: Callable[[], None] | None = None,
) -> StreamHandle:
    """Start a mocked recording stream and return its handle."""
    return _start_record(on_data, on_eof)


def stop_stream(handle: StreamHandle):
    """Stop a mocked recording stream by handle."""
    _stop_stream(handle)

