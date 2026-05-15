from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable
from urllib.parse import parse_qs

from config import AppConfig
from shortcut.types import Shortcut


def create_web_console_server(
    get_config: Callable[[], AppConfig],
    apply_config: Callable[[AppConfig], None],
    host: str = "127.0.0.1",
    port: int = 8936,
) -> ThreadingHTTPServer:
    class ConsoleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path != "/":
                self.send_error(404, "Not Found")
                return
            config = get_config()
            self._send_html(_render_page(config, message=""))

        def do_POST(self):
            if self.path != "/config":
                self.send_error(404, "Not Found")
                return

            content_len = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(content_len).decode("utf-8")
            form = parse_qs(body, keep_blank_values=True)
            shortcut_key = form.get("shortcut_key", [""])[0]
            model_path = form.get("model_path", [""])[0]
            raw_web_port = form.get("web_port", [""])[0]

            message = "Saved"
            try:
                web_port = int(raw_web_port)
                apply_config(
                    AppConfig(shortcut_key=Shortcut[shortcut_key], model_path=model_path, web_port=web_port)
                )
            except KeyError:
                message = "Error: unsupported shortcut_key"
            except ValueError as exc:
                message = f"Error: {exc}"

            self._send_html(_render_page(get_config(), message=message))

        def log_message(self, fmt: str, *args):
            return

        def _send_html(self, body: str):
            payload = body.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

    server = ThreadingHTTPServer((host, port), ConsoleHandler)

    return server


def _render_page(config: AppConfig, message: str) -> str:
    options = "".join(
        f'<option value="{name}"{" selected" if config.shortcut_key.name == name else ""}>{name}</option>'
        for name in Shortcut.__members__
    )
    is_error = message.startswith("Error:")
    status_class = "status error" if is_error else "status success"
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Voice Typer Console</title>
  <style>
    :root {{
      --bg: #f5f7fb;
      --card: #ffffff;
      --text: #1f2937;
      --muted: #6b7280;
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --border: #e5e7eb;
      --ok-bg: #ecfdf5;
      --ok-text: #065f46;
      --err-bg: #fef2f2;
      --err-text: #991b1b;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
    }}
    .wrap {{
      max-width: 700px;
      margin: 56px auto;
      padding: 0 20px;
    }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      box-shadow: 0 8px 28px rgba(0, 0, 0, 0.06);
      padding: 24px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 1.5rem;
    }}
    .subtitle {{
      margin: 0 0 20px;
      color: var(--muted);
      font-size: 0.95rem;
    }}
    .status {{
      padding: 10px 12px;
      border-radius: 10px;
      font-size: 0.92rem;
      margin-bottom: 16px;
    }}
    .status.success {{
      background: var(--ok-bg);
      color: var(--ok-text);
    }}
    .status.error {{
      background: var(--err-bg);
      color: var(--err-text);
    }}
    form {{
      display: grid;
      gap: 14px;
    }}
    label {{
      display: block;
      font-weight: 600;
      margin-bottom: 6px;
      font-size: 0.92rem;
    }}
    input, select {{
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px 12px;
      font-size: 0.95rem;
      background: #fff;
    }}
    input:focus, select:focus {{
      outline: 2px solid rgba(37, 99, 235, 0.2);
      border-color: var(--primary);
    }}
    button {{
      appearance: none;
      border: 0;
      border-radius: 10px;
      background: var(--primary);
      color: #fff;
      padding: 10px 16px;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      justify-self: start;
    }}
    button:hover {{
      background: var(--primary-hover);
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>Voice Typer Console</h1>
      <p class="subtitle">Update shortcut and model path, then apply immediately.</p>
      <p class="{status_class}">{escape(message)}</p>
      <form method="post" action="/config">
        <div>
          <label>Shortcut key</label>
          <select name="shortcut_key">{options}</select>
        </div>
        <div>
          <label>Model path</label>
          <input type="text" name="model_path" value="{escape(config.model_path)}"/>
        </div>
        <div>
          <label>Web console port</label>
          <input type="number" min="1" max="65535" name="web_port" value="{config.web_port}"/>
        </div>
        <button type="submit">Save</button>
      </form>
    </div>
  </div>
</body>
</html>
"""
