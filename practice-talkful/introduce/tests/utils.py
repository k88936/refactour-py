"""
Wrapper to use multiprocessing.Connection as stdin/stdout replacement.
Allows redirecting sys.stdin and sys.stdout to a bidirectional pipe.
"""
import sys
import time
from multiprocessing.connection import Connection


class ConnReader:
    """Wraps Connection to provide stdin-like interface for iteration"""
    def __init__(self, connection: Connection):
        self.conn = connection
        self.buffer = ""
    
    def __iter__(self):
        return self
    
    def __next__(self):
        while "\n" not in self.buffer:
            try:
                data = self.conn.recv()
                if data is None:  # EOF signal
                    if self.buffer:
                        result = self.buffer
                        self.buffer = ""
                        return result + "\n"
                    raise StopIteration
                self.buffer += data
            except EOFError:
                if self.buffer:
                    result = self.buffer
                    self.buffer = ""
                    return result + "\n"
                raise StopIteration
        
        line, self.buffer = self.buffer.split("\n", 1)
        return line + "\n"
    
    def readline(self):
        """Read a single line"""
        return next(self)


class ConnWriter:
    """Wraps Connection to provide stdout-like interface"""
    def __init__(self, connection: Connection):
        self.conn = connection
    
    def write(self, data: str):
        self.conn.send(data)
    
    def flush(self):
        pass
    
    def __iter__(self):
        return self
    
    def __next__(self):
        raise StopIteration


def redirect_stdio_to(conn: Connection) -> tuple[ConnReader, ConnWriter]:
    """
    Redirect sys.stdin and sys.stdout to use a multiprocessing Connection.
    
    Returns:
        Tuple of (reader, writer) that have been set as sys.stdin/stdout
    
    Example:
        def worker(conn):
            reader, writer = redirect_to_connection(conn)
            # Now sys.stdin reads from conn, sys.stdout writes to conn
            for line in sys.stdin:
                print(line)
    """
    reader = ConnReader(conn)
    writer = ConnWriter(conn)
    sys.stdin = reader
    sys.stdout = writer
    return reader, writer


def collect_output(conn: Connection, timeout: float = 0.3) -> str:
    """
    Collect all output from connection within the given timeout.

    Args:
        conn: multiprocessing.Connection to read from
        timeout: Time in seconds to collect output (default 0.3)

    Returns:
        Concatenated string of all received output

    Example:
        conn.send("shortcut 0 1\n")
        output = collect_output(conn)
        assert "1" in output
    """
    output = []
    start_time = time.time()

    while time.time() - start_time < timeout:
        if conn.poll(timeout=0.1):  # Check if data available with 50ms timeout
            try:
                data = conn.recv()
                if data is not None:
                    output.append(str(data))
            except EOFError:
                break
        else:
            time.sleep(0.1)  # Small sleep to avoid busy waiting

    return "".join(output)
