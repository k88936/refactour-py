from typing import Callable

from shortcut.types import Shortcut, ShortcutEvent
from shortcut._impl import _register_shortcut, _unregister_shortcut


def register_shortcut(shortcut: Shortcut, handler: Callable[[ShortcutEvent], None]):
    """Register a callback for a shortcut event stream."""
    _register_shortcut(shortcut, handler)


def unregister_shortcut(shortcut: Shortcut):
    """Unregister a previously registered shortcut callback."""
    _unregister_shortcut(shortcut)

