from enum import unique, Enum


@unique
class ShortcutEvent(Enum):
    PRESSED=0,
    RELEASED=1


@unique
class Shortcut(Enum):
    F1 = 0
    F2 = 1
    F3 = 2
    F4 = 3
    F5 = 4
    F6 = 5
    F7 = 6
    F8 = 7
