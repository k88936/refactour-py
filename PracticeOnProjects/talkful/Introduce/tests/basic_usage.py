import multiprocessing
import unittest

from talkful_test_utils import redirect_stdio_to, collect_output


def voice_typer_demo(conn):
    from main import main
    redirect_stdio_to(conn)
    main()


class VoiceTyperTest(unittest.TestCase):
    def setUp(self):
        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.p = multiprocessing.Process(target=voice_typer_demo, args=(self.child_conn,))
        self.p.start()

    def tearDown(self):
        if self.parent_conn:
            self.parent_conn.close()
        if self.p.is_alive():
            self.p.terminate()
            self.p.join(timeout=1)
            if self.p.is_alive():
                self.p.kill()

    def test_press_record_release_injects_asr_text(self):
        samples = [0.2, 0.4, 0.6]

        self.parent_conn.send("shortcut F1 PRESSED\n")
        for sample in samples:
            self.parent_conn.send(f"voice {sample}\n")
        self.parent_conn.send("shortcut F1 RELEASED\n")

        output = collect_output(self.parent_conn)
        self.assertIn(f"inject", output)


if __name__ == "__main__":
    unittest.main()
