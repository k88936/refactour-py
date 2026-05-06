from enum import unique, IntEnum


@unique
class ShortcutEvent(IntEnum):
    PRESSED = 1
    RELEASED = 2


@unique
class Shortcut(IntEnum):
    F1 = 0
    F2 = 1
    F3 = 2
    F4 = 3
    F5 = 4
    F6 = 5
    F7 = 6
    F8 = 7
