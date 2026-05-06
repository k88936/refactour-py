import multiprocessing
import os
import tempfile
import unittest
from pathlib import Path

from tests.utils import redirect_stdio_to, collect_output


def voice_typer_demo_in_workdir(conn, workdir: str):
    from main import main

    os.chdir(workdir)
    redirect_stdio_to(conn)
    main()


class VoiceTyperConfigTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        workdir = Path(self.temp_dir.name)
        (workdir / "config.json").write_text('{"shortcut_key":"F2","model_path":"custom_model.txt"}', encoding="utf-8")
        (workdir / "custom_model.txt").write_text("mock custom model", encoding="utf-8")

        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.p = multiprocessing.Process(target=voice_typer_demo_in_workdir, args=(self.child_conn, self.temp_dir.name))
        self.p.start()

    def tearDown(self):
        if self.parent_conn:
            self.parent_conn.close()
        if self.p.is_alive():
            self.p.terminate()
            self.p.join(timeout=1)
            if self.p.is_alive():
                self.p.kill()
        self.temp_dir.cleanup()

    def test_configured_shortcut_is_used(self):
        samples = [0.3, 0.5]

        self.parent_conn.send("shortcut F1 PRESSED\n")
        for sample in samples:
            self.parent_conn.send(f"voice {sample}\n")
        self.parent_conn.send("shortcut F1 RELEASED\n")
        output_with_f1 = collect_output(self.parent_conn)
        self.assertNotIn("inject", output_with_f1)

        self.parent_conn.send("shortcut F2 PRESSED\n")
        for sample in samples:
            self.parent_conn.send(f"voice {sample}\n")
        self.parent_conn.send("shortcut F2 RELEASED\n")
        output_with_f2 = collect_output(self.parent_conn)
        self.assertIn("inject", output_with_f2)

if __name__ == "__main__":
    unittest.main()
