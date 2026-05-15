from asr._impl import _load_model, _recognize, _unload_model
from asr.types import AsrModelHandle


def load_model(path: str) -> AsrModelHandle:
    """Load an ASR model from the filesystem path and return a model handle."""
    return _load_model(path)


def unload_model(handle: AsrModelHandle):
    """Unload a previously loaded ASR model handle."""
    return _unload_model(handle)


def recognize(samples: list[float], model_handle: AsrModelHandle) -> str:
    """Recognize text from audio samples using the given model handle."""
    return _recognize(samples, model_handle)
