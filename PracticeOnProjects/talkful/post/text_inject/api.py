from text_inject._impl import _inject_text


def inject_text(text: str):
    """
    Inject text into the current focused input area
    """
    _inject_text(text)
