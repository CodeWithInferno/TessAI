from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input
from rich.markdown import Markdown
import asyncio
import requests
import platform
from pathlib import Path
from uuid import uuid4
import os

from widgets import TessMessage

# === Server info ===
SERVER_URL = "https://chances-gave-albert-risk.trycloudflare.com"
CHAT_ENDPOINT = f"{SERVER_URL}/chat"
DEVICE_ID_FILE = os.path.join(str(Path.home()), "TessAI", "device_id.txt")

def get_device_id():
    if os.path.exists(DEVICE_ID_FILE):
        with open(DEVICE_ID_FILE, "r") as f:
            return f.read().strip()
    else:
        device_id = f"{platform.system()}_{platform.node()}_{uuid4().hex[:8]}"
        with open(DEVICE_ID_FILE, "w") as f:
            f.write(device_id)
        return device_id

DEVICE_ID = get_device_id()

async def call_tess(query: str) -> str:
    try:
        res = requests.post(CHAT_ENDPOINT, json={"query": query, "device_id": DEVICE_ID})
        res.raise_for_status()

        print("🪵 Server response:", res.text)  # Raw response for debugging
        json_data = res.json()
        return json_data.get("response") or json_data.get("message") or "No reply."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

class TessUI(App):
    CSS_PATH = "style.css"
    BINDINGS = [("ctrl+c", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield VerticalScroll(id="chat")
        yield Input(placeholder="Type your message to Tess...", id="input")

    async def on_input_submitted(self, message: Input.Submitted) -> None:
        query = message.value.strip()
        chat = self.query_one("#chat", VerticalScroll)
        self.query_one("#input", Input).value = ""

        await chat.mount(TessMessage("You", query))

        thinking = TessMessage("Tess", "_Tess is thinking..._", thinking=True)
        await chat.mount(thinking)
        await asyncio.sleep(0.4)

        response = await call_tess(query)

        await thinking.remove()
        await chat.mount(TessMessage("Tess", response.strip()))
        chat.scroll_end(animate=False)

if __name__ == "__main__":
    TessUI().run()
