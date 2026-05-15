import multiprocessing
import os
import socket
import tempfile
import time
import unittest
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from talkful_test_utils import collect_output, redirect_stdio_to


def _find_free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def voice_typer_demo_in_workdir_web(conn, workdir: str):
    from main import main

    os.chdir(workdir)
    redirect_stdio_to(conn)
    main()


class VoiceTyperWebConsoleTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        workdir = Path(self.temp_dir.name)
        self.port = _find_free_port()
        (workdir / "config.json").write_text(
            f'{{"shortcut_key":"F1","model_path":"model_v1.txt","web_port":{self.port}}}',
            encoding="utf-8",
        )
        (workdir / "model_v1.txt").write_text("mock model v1", encoding="utf-8")
        (workdir / "model_v2.txt").write_text("mock model v2", encoding="utf-8")

        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.p = multiprocessing.Process(
            target=voice_typer_demo_in_workdir_web,
            args=(self.child_conn, self.temp_dir.name),
        )
        self.p.start()
        self._wait_console_up()

    def tearDown(self):
        if self.parent_conn:
            self.parent_conn.close()
        if self.p.is_alive():
            self.p.terminate()
            self.p.join(timeout=1)
            if self.p.is_alive():
                self.p.kill()
        self.temp_dir.cleanup()

    def _wait_console_up(self):
        url = f"http://127.0.0.1:{self.port}/"
        last_error = None
        for _ in range(20):
            try:
                with urlopen(url, timeout=0.5) as resp:
                    if resp.status == 200:
                        return
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                time.sleep(0.1)
        raise RuntimeError(f"Web console did not start: {last_error}")

    def test_web_console_updates_config_and_effect_immediately(self):
        update_data = urlencode(
            {"shortcut_key": "F2", "model_path": "model_v2.txt", "web_port": str(self.port)}
        ).encode("utf-8")
        request = Request(
            f"http://127.0.0.1:{self.port}/config",
            data=update_data,
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with urlopen(request, timeout=1.0) as resp:
            body = resp.read().decode("utf-8")
            self.assertIn("Saved", body)

        self.parent_conn.send("shortcut F1 PRESSED\n")
        self.parent_conn.send("voice 0.3\n")
        self.parent_conn.send("shortcut F1 RELEASED\n")
        output_f1 = collect_output(self.parent_conn)
        self.assertNotIn("inject", output_f1)

        self.parent_conn.send("shortcut F2 PRESSED\n")
        self.parent_conn.send("voice 0.5\n")
        self.parent_conn.send("shortcut F2 RELEASED\n")
        output_f2 = collect_output(self.parent_conn)
        self.assertIn("inject", output_f2)

        saved = (Path(self.temp_dir.name) / "config.json").read_text(encoding="utf-8")
        self.assertIn('"shortcut_key": "F2"', saved)
        self.assertIn('"model_path": "model_v2.txt"', saved)
        self.assertIn(f'"web_port": {self.port}', saved)


if __name__ == "__main__":
    unittest.main()
