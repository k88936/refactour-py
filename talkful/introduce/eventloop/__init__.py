from eventloop._impl import _eventloop


def eventloop():
    """Run the event loop and dispatch incoming mocked events."""
    _eventloop()
