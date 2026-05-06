from dataclasses import dataclass


@dataclass
class AsrModelHandle:
    model_path: str
    model_data: str
