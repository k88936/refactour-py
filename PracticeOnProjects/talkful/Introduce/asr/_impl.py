import random
from pathlib import Path

from asr.types import AsrModelHandle


def _load_model(path: str) -> AsrModelHandle:
    model_data = Path(path).read_text(encoding="utf-8")
    return AsrModelHandle(model_path=path, model_data=model_data)


def _unload_model(handle: AsrModelHandle):
    return None


def _recognize(samples: list[float], model_handle: AsrModelHandle) -> str:
    """
    Mocked ASR processor. 
    
    Takes audio samples and returns a mocked recognized text.
    In a real system, this would run ML inference on the audio.
    """
    if not samples:
        return ""
    
    # Mock phrases for demo purposes
    mock_phrases = [
        "hello world",
        "this is a test",
        "mocked recognition",
        "voice input demo",
        "audio sample processing",
    ]
    
    # Include model identity/content in seed so different models can produce different outputs.
    seed = int(sum(samples) * 1000) + sum(ord(c) for c in model_handle.model_data)
    random.seed(seed % (2**31))
    result = random.choice(mock_phrases)
    random.seed()  # Reset seed
    
    return result
