from typing import Callable

from shortcut.types import Shortcut, ShortcutEvent

_registered_shortcuts: dict[Shortcut, Callable[[ShortcutEvent], None]] = {}


def _register_shortcut(shortcut: Shortcut, handler: Callable[[ShortcutEvent], None]):
    _registered_shortcuts[shortcut] = handler


def _unregister_shortcut(shortcut: Shortcut):
    _registered_shortcuts.pop(shortcut, None)


def _try_handle_shortcut_events(raw_event: str) -> bool:
    """
    format: shortcut {id:int} {event:int}
    """
    tokens = raw_event.strip().split()
    if not tokens or tokens[0] != "shortcut":
        return False
    
    shortcut = Shortcut(int(tokens[1]))
    event = ShortcutEvent(int(tokens[2]))
    handler = _registered_shortcuts.get(shortcut)
    if handler:
        handler(event)
    return True

