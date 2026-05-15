import multiprocessing
import time
import unittest

from talkful_test_utils import collect_output, redirect_stdio_to

def audio_demo(conn):
    redirect_stdio_to(conn)

    from eventloop import eventloop
    from audio.api import start_record

    def on_data(samples: list[float]):
        print(f"SAMPLE:{samples[0]}")

    def on_eof():
        print("EOF")

    start_record(on_data, on_eof)
    print("STREAM_STARTED")
    eventloop()


def audio_stop_demo(conn):
    redirect_stdio_to(conn)

    from audio.api import start_record, stop_stream

    def on_data(samples: list[float]):
        print(f"SAMPLE:{samples[0]}")

    def on_eof():
        print("EOF")

    handle = start_record(on_data, on_eof)
    stop_stream(handle)


def audio_concurrent_demo(conn):
    redirect_stdio_to(conn)

    from eventloop import eventloop
    from audio.api import start_record

    def on_data_1(samples: list[float]):
        print(f"S1:{samples[0]}")

    def on_data_2(samples: list[float]):
        print(f"S2:{samples[0]}")

    start_record(on_data_1)
    start_record(on_data_2)
    print("STREAMS_STARTED")
    eventloop()


class AudioTest(unittest.TestCase):
    def setUp(self):
        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.p = multiprocessing.Process(target=audio_demo, args=(self.child_conn,))
        self.p.start()

    def tearDown(self):
        if self.parent_conn:
            self.parent_conn.close()
        if self.p.is_alive():
            self.p.terminate()
            self.p.join(timeout=1)
            if self.p.is_alive():
                self.p.kill()

    def test_stream_starts(self):
        output = collect_output(self.parent_conn)
        self.assertIn("STREAM_STARTED", output)

    def test_voice_event_triggers_callback(self):
        self.parent_conn.send("voice 0.5\n")
        output = collect_output(self.parent_conn)
        self.assertIn("SAMPLE:0.5", output)

    def test_invalid_voice_value_exits(self):
        self.parent_conn.send("voice invalid\n")
        time.sleep(0.3)
        self.p.join(timeout=1)
        self.assertFalse(self.p.is_alive())


class AudioLifecycleTest(unittest.TestCase):
    def test_stop_stream_triggers_eof(self):
        parent_conn, child_conn = multiprocessing.Pipe()
        p = multiprocessing.Process(target=audio_stop_demo, args=(child_conn,))
        p.start()
        output = collect_output(parent_conn)

        parent_conn.close()
        p.join(timeout=1)
        if p.is_alive():
            p.terminate()
            p.join(timeout=1)

        self.assertIn("EOF", output)


class AudioConcurrentTest(unittest.TestCase):
    def setUp(self):
        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.p = multiprocessing.Process(target=audio_concurrent_demo, args=(self.child_conn,))
        self.p.start()

    def tearDown(self):
        if self.parent_conn:
            self.parent_conn.close()
        if self.p.is_alive():
            self.p.terminate()
            self.p.join(timeout=1)
            if self.p.is_alive():
                self.p.kill()

    def test_multiple_streams_receive_same_voice_event(self):
        self.parent_conn.send("voice 0.75\n")
        output = collect_output(self.parent_conn)
        self.assertIn("S1:0.75", output)
        self.assertIn("S2:0.75", output)


if __name__ == "__main__":
    unittest.main()
