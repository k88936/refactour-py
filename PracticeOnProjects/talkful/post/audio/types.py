from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StreamHandle:
    _id: int
