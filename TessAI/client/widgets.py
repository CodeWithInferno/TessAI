from textual.widgets import Static
from textual.containers import Vertical
from rich.markdown import Markdown
from textual.app import ComposeResult

class TessMessage(Vertical):
    def __init__(self, role: str, message: str, thinking: bool = False):
        super().__init__()
        self.role = role
        self.message = message
        self.thinking = thinking

    def compose(self) -> ComposeResult:
        header_text = f"[bold magenta]{self.role}[/bold magenta]" if self.role.lower() == "tess" else f"[bold cyan]{self.role}[/bold cyan]"
        yield Static(header_text)

        if self.thinking:
            yield Static(Markdown("_Tess is thinking..._"), classes="chat-think")
        else:
            yield Static(Markdown(self.message), classes="chat-bubble")
