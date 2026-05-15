import sys

from audio._impl import _try_handle_voice_events
from shortcut._impl import _try_handle_shortcut_events


def _eventloop():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        if _try_handle_shortcut_events(line):
            continue
        if _try_handle_voice_events(line):
            continue

        # If not handled by any handler, raise error
        raise RuntimeError(f"Unhandled event: {line}")
